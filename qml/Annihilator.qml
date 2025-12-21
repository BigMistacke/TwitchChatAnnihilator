import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    property bool running: false

    RowLayout {
        anchors.fill: parent


        ColumnLayout {
            ComboBox {
                id: ruleSetCombo
                Layout.preferredWidth: 300
                model: DataModel.rule_list
                currentIndex: DataModel.current_rule_index

                onActivated: function(index) {
                    EventHandler.select_rule(index)
                }
            }

            Button {
                text: TwitchModel.is_running ? "Show Mercy" : "Commence Annihilation"
                Layout.preferredWidth: 300
                Layout.fillHeight: true
                font.pixelSize: 24

                background: Rectangle {
                    anchors.fill: parent
                    color: {
                        if(TwitchModel.is_running){
                            parent.down ? darkenColor("#12e04c", 0.3) : (parent.hovered ? "#12e04c" : darkenColor("#12e04c", 0.1))
                        }else {
                            parent.down ? darkenColor("#a81b1b", 0.3) : (parent.hovered ? "#a81b1b" : darkenColor("#a81b1b", 0.1))
                        }
                    }
                }
                onClicked: {
                    if(TwitchModel.is_running){
                        EventHandler.stop_ban_bot()
                    }else {
                        EventHandler.start_ban_bot()
                    }
                }
            }
        }

        Rectangle {
            id: timeoutBlock
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#eeeeee"
            border.color: "#cccccc"

            Text {
                id: timeoutText
                anchors.centerIn: parent
                text: "All is quiet"
                wrapMode: Text.WordWrap
            }
        }
    }

    Connections {
        target: TimeoutInfo

        function onTimeoutInfoUpdated(username, message, reason, duration, acceptable) {
            timeoutText.text = message

            if(acceptable){
                timeoutBlock.color = "red"
            }else{
                timeoutBlock.color = "green"
            }
        }
    }

    function darkenColor(color, percent) {
        var c = Qt.darker(color, 1 + percent)
        return c
    }
}
