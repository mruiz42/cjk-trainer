import QtQml 2.1
import QtQuick 2.0

Flipable {
    id:myFlip
    x:0
    y:0
    width: 800
    height:430

    function showFront() {
        rot.angle=0;
    }

    function showBack() {
        rot.angle=180;
    }
    transform: Rotation {
                id: rot
                origin.x: 400;
                origin.y:215;
                axis.x:1; axis.y:0; axis.z:0
                angle:0

                Behavior on angle { PropertyAnimation{} }
            }
    front: Item {
                Rectangle {
                    width: 800
                    height: 430
                    color:"lightsteelblue"
                }

                Text {
                    x: 0
                    y:200
                    text: "Side A"
                }
            }

back: Item {

        transform:Rotation {
            origin.x: 400;
            origin.y:215;
            axis.x:1; axis.y:0; axis.z:0
            angle:180
        }

        Rectangle {
             width: 800
             height: 430
             color:"lightsteelblue"
        }

        Text {
            x: 0
            y:200
            text: "Side B"
        }
    }
    MouseArea {
        anchors.fill: parent
        onPressed: { myFlip.showBack(); }
        onReleased: { myFlip.showFront(); }
    }


}