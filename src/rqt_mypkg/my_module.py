
import os
import rospy
import rospkg

from std_msgs.msg import String
from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget

class MyPlugin(Plugin):

    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('MyPlugin')
        # Create publisher
        self.signal_publisher = rospy.Publisher('/gui_signal', String, queue_size=10)
        self.speech_publisher = rospy.Publisher('/speech_content', String, queue_size=10)
        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser
        parser.add_argument("-q", "--quiet", action="store_true",
                            dest="quiet",
                            help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_mypkg'), 'resource', 'MyPlugin.ui')
        # Extend the widget with all atrributes and children from UI File
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('MyPluginUi')
        # Show _widget.windowTitle on left-top of each plugin(when it's set in _widget).
        # This is useful when you open multiple plugins aat once. Also if you open multiple
        # instances of your plugin at once, these lines add number to make it easy to
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' %d' % context.serial_number()))
        else:
            self._widget.setWindowTitle(self._widget.windowTitle())
        # Add widget to the user interface
        context.add_widget(self._widget)
        self._widget.stopButton.clicked[bool].connect(self.__handle_stop_clicked)
        self._widget.startButton.clicked[bool].connect(self.__handle_start_clicked)
        self._widget.standbyButton.clicked[bool].connect(self.__handle_standby_clicked)
        self._widget.talkButton.clicked[bool].connect(self.__handle_talk_clicked)

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.get_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    def __handle_standby_clicked(self):
        msg = String()
        msg.data = 'STANDBY'
        self.signal_publisher.publish(msg)
        rospy.loginfo("STANDBY Button is clicked")
        
    def __handle_stop_clicked(self):
        msg = String()
        msg.data = 'STOP'
        self.signal_publisher.publish(msg)
        rospy.loginfo("STOP Button is clicked")

    def __handle_start_clicked(self):
        msg = String()
        msg.data = 'START'
        self.signal_publisher.publish(msg)
        rospy.loginfo("START Button is clicked")

    def __handle_talk_clicked(self):
        msg = String()
        msg.data = self._widget.speechText.text()
        self.speech_publisher.publish(msg)
        rospy.loginfo('TALK Button is clicked: {}'.format(msg.data))
