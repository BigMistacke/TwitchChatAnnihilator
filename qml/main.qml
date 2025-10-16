import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    title: qsTr("Twitch Chat Annihilator")

    // Top Navigation Bar
    header: ToolBar {
        RowLayout {
            ToolButton {
                text: "Main"
                onClicked: stackView.push(mainPage)
            }

            ToolButton {
                text: "Rules"
                onClicked: stackView.push(rulesPage)
            }

            ToolButton {
                text: "Lexicons"
                onClicked: stackView.push(lexiconPage)
            }

            ToolButton {
                text: "Settings"
                onClicked: stackView.push(settingsPage)
            }
        }
    }

    StackView {
        id: stackView
        anchors.fill: parent

        initialItem: mainPage
    }

    // Main Page
    Component {
        id: mainPage

        Annihilator {
        }
    }

    // Rules Page
    Component {
        id: rulesPage

        Rules {

        }
    }

    // Lexicon Page
    Component {
        id: lexiconPage

        Lexicons {

        }
    }

    // Settings Page
    Component {
        id: settingsPage

        Settings {

        }
    }
}
