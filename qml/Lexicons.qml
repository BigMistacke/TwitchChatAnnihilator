import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Item {
    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        ComboBox {
            id: lexiconSelector
            Layout.preferredWidth: 300
            model: ["Lexicon A", "Lexicon B", "Lexicon C"]
        }

        TextArea {
            id: lexiconEditor
            Layout.fillWidth: true
            Layout.fillHeight: true
            placeholderText: "Edit lexicon here..."
        }
    }
}
