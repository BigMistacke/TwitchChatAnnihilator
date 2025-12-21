import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

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
                    EventHandler.delete_lexicon()
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
                        EventHandler.save_lexicon_as(lexiconEditor.text, fileNameField.text)
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

    FileDialog {
        id: fileDialog
        currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
        nameFilters: ["Text files (*.txt)"]
        onAccepted: EventHandler.import_lexicon(selectedFile)
    }


    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        RowLayout {
            ComboBox {
                id: lexiconSelector
                Layout.preferredWidth: 300
                model: DataModel.lexicon_list
                currentIndex: DataModel.current_lexicon_index

                onActivated: function(index) {
                    EventHandler.select_lexicon(index)
                }
            }

            Button {
                text: "Save"
                onClicked: {
                    EventHandler.save_lexicon(lexiconEditor.text)
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
                    EventHandler.new_lexicon()
                }
            }

            Button {
                text: "Import"
                onClicked: {
                    fileDialog.open()
                }
            }
        }


        ScrollView {
            id: view
            Layout.fillWidth: true
            Layout.fillHeight: true

            TextArea {
                id: lexiconEditor
                Layout.fillWidth: true
                Layout.fillHeight: true
                wrapMode: Text.WordWrap
                placeholderText: "Edit lexicon here..."
                text: DataModel.current_lexicon
            }
        }
    }
}
