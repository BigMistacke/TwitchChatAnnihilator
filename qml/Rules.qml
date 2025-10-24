import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    ColumnLayout {
        anchors.fill: parent
        spacing: 10


        RowLayout {
            spacing: 10

            ComboBox {
                id: ruleSetCombo
                Layout.preferredWidth: 300
                model: DataModel.rule_list
                currentIndex: DataModel.current_index

                onActivated: function(index) {
                    EventHandler.select_rule(index)
                }
            }

            Button {
                text: "Save"
                onClicked: {
                    EventHandler.save_rule(ruleEditor.text)
                }
            }

            Button {
                text: "Save as"
            }

            Button {
                text: "Delete"
            }

            Button {
                text: "New"
            }

            Button {
                text: "Run Test"

            }
        }

        TextArea {
            id: ruleEditor
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: DataModel.current_rule
            placeholderText: "Rule instructions"

            background: Rectangle {
                anchors.fill: parent
                color: "dimgray"
            }

            Keys.onPressed: function(event) {
                if (event.key === Qt.Key_Escape) {
                    focus = false
                    event.accepted = true
                }
            }
        }

        TextArea {
            id: testCaseEditor
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            placeholderText: "Test case..."

            background: Rectangle {
                anchors.fill: parent
                color: "dimgray"
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            color: "#eeeeee"
            border.color: "#cccccc"

            Text {
                anchors.centerIn: parent
                text: ""
                wrapMode: Text.WordWrap
            }
        }
    }
}
