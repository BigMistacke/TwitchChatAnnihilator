import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15



Item {
    ColumnLayout {
        anchors.centerIn: parent
        spacing: 10

        Label {
            text: "Settings Page"
        }


        Button {
            text: "Login"

            onClicked: {
                var url = EventHandler.login()
                Qt.openUrlExternally(url)
            }
        }

        TextField {
            id: channelName
            placeholderText: qsTr("Target Channel")

            onTextChanged: debounceTimer.restart()

            Keys.onPressed: function(event) {
                if (event.key === Qt.Key_Escape) {
                    focus = false
                    event.accepted = true
                }
            }

            Timer {
                id: debounceTimer
                interval: 1000   // adjust delay in ms as needed
                repeat: false
                onTriggered: EventHandler.set_channel(channelName.text)
            }
        }

    }
}
