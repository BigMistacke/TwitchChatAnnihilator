import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15



Item {
    Popup {
        id: linkPopup
        anchors.centerIn: Overlay.overlay
        width: 500
        height: 100
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent


        ColumnLayout {
            anchors.centerIn: parent

            Label {
                id: codeLabel
                text: "Please go to the link below and enter the following code: "
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                id: linkLabel
                text: "<a href='http://www.twitch.tv'>twitch.tv</a>"
                onLinkActivated: Qt.openUrlExternally(link)
                Layout.alignment: Qt.AlignHCenter
            }

            Button {
                text: "close"
                onClicked: linkPopup.close()
                Layout.alignment: Qt.AlignHCenter
            }
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 10

        Label {
            text: "Settings Page"
        }

        Label {
            id: loginText
            visible: TwitchModel.current_login
            text: { TwitchModel.current_login ? TwitchModel.current_user : ""}
        }
        Button {
            text: {
                TwitchModel.current_login ? "Logout" : "Login"
            }

            onClicked: {
                if(!TwitchModel.current_login) {
                    var result = EventHandler.login()

                    linkLabel.text = "<a href='" + result.url + "'>" + result.url + "</a>"
                    codeLabel.text = "Please login using the link below and enter the following code: " + result.code
                    linkPopup.open()
                } else{
                    EventHandler.logout()
                }
            }
        }


        TextField {
            id: channelName
            placeholderText: qsTr("Target Channel")
            text: TwitchModel.current_channel

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
