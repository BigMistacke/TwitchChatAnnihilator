import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {

    Popup {
        id: confirmPopup
        width: 175
        height: 75
        dim: true
        focus: true
        modal: true

        anchors.centerIn: Overlay.overlay
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        background: Rectangle {
            anchors.fill: parent
            color: "#595959"
            radius: 8
            border.color: "#cccccc"
            border.width: 1

        }

        Overlay.modal: Rectangle {
            color: "#80333333"
        }

        RowLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Button {
                text: "Confirm"

                onClicked: {
                    confirmPopup.close();
                    EventHandler.delete_rule()
                }

                background: Rectangle {
                    color: parent.down ? "#80ffffff" : (parent.hovered ? "#4dffffff" : "#00ffffff")
                    radius: 6
                    border.width: parent.hovered ? 1 : 0
                    border.color: "white"
                }
            }

            Button {
                text: "Cancel"

                onClicked: {
                    confirmPopup.close()
                }

                background: Rectangle {
                    color: parent.down ? "#80ffffff" : (parent.hovered ? "#4dffffff" : "#00ffffff")
                    radius: 6
                    border.width: parent.hovered ? 1 : 0
                    border.color: "white"
                }
            }
        }
    }

    Popup {
        id: renamePopup
        width: 250
        height: 130
        dim: true
        focus: true
        modal: true

        anchors.centerIn: Overlay.overlay
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        background: Rectangle {
            anchors.fill: parent
            color: "#595959"
            radius: 8
            border.color: "#cccccc"
            border.width: 1
        }

        Overlay.modal: Rectangle {
            color: "#80333333"
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Label {
                text: "Rename to"
                font.bold: true
                color: "white"
                Layout.alignment: Qt.AlignHCenter
            }

            TextField {
                id: fileNameField
                placeholderText: "Enter file name..."
                Layout.fillWidth: true
            }

            RowLayout {
                spacing: 12
                Layout.alignment: Qt.AlignCenter

                Button {
                    text: "Save"

                    onClicked: {
                        EventHandler.save_rule_as(ruleEditor.text, fileNameField.text)
                        renamePopup.close();
                    }

                    background: Rectangle {
                        color: parent.down ? "#80ffffff" : (parent.hovered ? "#4dffffff" : "#00ffffff")
                        radius: 6
                        border.width: parent.hovered ? 1 : 0
                        border.color: "white"
                    }
                }

                Button {
                    text: "Cancel"

                    onClicked: {
                        renamePopup.close()
                    }

                    background: Rectangle {
                        color: parent.down ? "#80ffffff" : (parent.hovered ? "#4dffffff" : "#00ffffff")
                        radius: 6
                        border.width: parent.hovered ? 1 : 0
                        border.color: "white"
                    }
                }
            }
        }
    }


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
                text: "Rename"
                onClicked: renamePopup.open()

            }

            Button {
                text: "Delete"
                onClicked: confirmPopup.open()
            }

            Button {
                text: "New"
                onClicked: {
                    EventHandler.new_rule()
                }
            }

            Button {
                text: "Run Test"
                onClicked: {
                    EventHandler.test_rule(ruleEditor.text, testCaseEditor.text)
                }
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
