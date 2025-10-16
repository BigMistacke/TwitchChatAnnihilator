import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        TextArea {
            id: dslEditor
            Layout.fillWidth: true
            Layout.fillHeight: true
            placeholderText: "Write your DSL here..."

            background: Rectangle {
                anchors.fill: parent
                color: "dimgray"
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

        RowLayout {
            spacing: 10

            Button {
                text: "Run Test"
                onClicked: {
                    // Your logic here
                }
            }

            Button {
                text: "New"
            }

            Button {
                text: "Save"
            }

            Button {
                text: "Load"
            }
        }
    }
}
