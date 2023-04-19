import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 400)
        self.upload_button = QPushButton('Upload', self)
        self.upload_button.clicked.connect(self.upload_image)
        self.bounding_boxes = []
        self.drawing = False

        # Set up main window
        self.setWindowTitle('Bounding Box Tool')
        self.setFixedSize(500, 500)

    def upload_image(self):
        # Get image file path from user
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')

        if file_path:
            # Display selected image
            pixmap = QPixmap(file_path).scaled(self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.drawing:
            # Start drawing bounding box
            self.drawing = True
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            # Draw bounding box
            pixmap = self.image_label.pixmap()
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(self.start_pos.x(), self.start_pos.y(),
                              event.x() - self.start_pos.x(), event.y() - self.start_pos.y())
            self.image_label.setPixmap(pixmap)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            # Finish drawing bounding box
            self.drawing = False
            self.bounding_boxes.append({
                'x1': self.start_pos.x(),
                'y1': self.start_pos.y(),
                'x2': event.x(),
                'y2': event.y()
            })

    
    
    
    #def upload_image(self):
        # if not self.bounding_boxes:
        #     return

        # # Get image file path from user
        # file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')

        # if file_path:
        #     # Send image and bounding box data to server
        #     with open(file_path, 'rb') as f:
        #         files = {'image': f}
        #         data = {'bounding_boxes': self.bounding_boxes}
        #         response = requests.post('http://your-server.com/upload', files=files, data=data)

        #         if response.status_code == 200:
        #             print('Image uploaded successfully!')
        #pass

    def closeEvent(self, event):
        # Prompt user to save bounding box data before closing
        reply = QMessageBox.question(self, 'Save Bounding Box Data',
                                      'Do you want to save the bounding box data before closing?',
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            # Save bounding box data to file
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save Bounding Box Data', '', 'Text Files (*.txt)')
            if file_path:
                with open(file_path, 'w') as f:
                    for box in self.bounding_boxes:
                        f.write(f'{box["x1"]},{box["y1"]},{box["x2"]},{box["y2"]}\n')
                print('Bounding box data saved successfully!')

        elif reply == QMessageBox.Cancel:
            event.ignore()
            return

        # Close the main window
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())