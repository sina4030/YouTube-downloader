#sina-talebi
import rc_photo
from PyQt6 import QtWidgets, QtCore, QtNetwork
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
#It is for communication with the tor
import stem.process
from pytube import Playlist
from pytube import YouTube as YT
import threading as th
import time
from stem.control import Controller
from stem import CircStatus,Signal 
from datetime import datetime

import sockschain,socks,socket,pipwin,time,humanize,pafy,urllib.request,youtube_dl,os,io,urllib.error,json,requests,re
from fake_useragent import UserAgent
from urllib.request import urlopen
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PySide6.QtWidgets import QApplication, QProxyStyle
import os,sys,threading,urllib3,http.client
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.uic import loadUiType 
from pytube import Playlist

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        # call the parent class constructor and pass the parent argument
        super(MainApp, self).__init__(parent)
        # call the constructors of QMainWindow and ui classes
        QMainWindow.__init__(self)
        self.setupUi(self)
        # initialize the UI and button connections
        self.InitUI()
        self.Handel_Buttons()
        
    def InitUI(self):
        # remove the tabs bar from the UI
        self.tabWidget.tabBar().setVisible(False)

    # apply the default style of the app (DarkOrange)
        self.Apply_DarkOrange_Style()

    # move each UI element to its initial position
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()

    def Handel_Buttons(self):

        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)
        self.pushButton_8.clicked.connect(self.Open_Home)
        self.pushButton_11.clicked.connect(self.Open_Youtube)
        self.pushButton_10.clicked.connect(self.Open_Settings)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_Style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_15.clicked.connect(self.Apply_QDarkBlue_Style)


    ##############################################
    # Download Youtube Single Video
    def Save_Browse(self):
        # open a file dialog to select a save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)")
    # retrieve the file path and set it in the QLineEdit
        self.lineEdit_4.setText(str(save_location[0]))

    def Get_Video_Data(self):
        # retrieve video URL from QLineEdit
        video_url = self.lineEdit_3.text()
        print(video_url)

    # check if URL is valid
        if video_url == '':
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid Video URL")

        else:
            # create a pafy object for the video
            video = pafy.new(video_url)

            # print video metadata
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            # retrieve available video streams
            video_streams = video.videostreams
            for stream in video_streams:
                # retrieve filesize and convert to a human-readable string
                size = humanize.naturalsize(stream.get_filesize())

                if 'DASH' not in stream.extension:

                    data = "{} {} {} {}".format(
                        stream.mediatype, stream.extension, stream.quality, size)
                # add the string to the combo box
                self.comboBox.addItem(data)

    def Download_Video(self):
        # Get the video URL and save location from the corresponding QLineEdit widgets
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

     # Check if both fields are not empty
        if video_url == '' or save_location == '':
            # Show a warning message box if either field is empty
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid Video URL or save location")
        else:
            # Use the pafy library to get the video object based on the URL
            video = pafy.new(video_url)
            # Get the available video streams
            best_streams = video.getbest()
            # Get the selected video quality from the combobox

            # Start the video download with the selected stream and callback the progress function
            download = best_streams.download(
                filepath=save_location, callback=self.Video_Progress)

     # Define the function to update the progress bar and label

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received

    # If the total download size is greater than 0...
        if total > 0:
            # Calculate the download percentage and set it as the value of the progress bar
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(int(download_percentage))

            # Calculate the remaining time and display it as a label
            remaining_time = round((time / 1024) / 60, 2)

            self.label_5.setText(
                str('{} minutes remaining'.format(remaining_time)))

            # Process any pending events to update the progress bar and label
            QApplication.processEvents()

    ################################################
    # Youtube Playlist Download
    # Define a function called Playlist_Download which accepts self as a parameter
    def Playlist_Download(self, quality):
        # Get user input from two text boxes, one for playlist URL and one for save location
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        # Create the output directory
        output_dir = os.path.join(save_location, "youtube_playlist")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Download the playlist
        playlist = Playlist(playlist_url)
        videos = playlist.videos
        for video in videos:
            video_streams = video.streams.filter(
                progressive=True, file_extension='mp4', res=quality).last()
            file_size = video_streams.filesize
            print(f"Downloading {video.title} of size {file_size} bytes")
            video_streams.download(output_path=output_dir)

        print("Download Complete!")

        try:
            playlist = pafy.get_playlist(playlist_url)
        except urllib.error.HTTPError as e:
            QMessageBox.warning(self, "HTTP Error",
                                f"Failed to retrieve playlist: {e}")
        else:
            playlist_videos = playlist['items']
            

    # Initialize a variable called "current_video_in_download" to keep track of how many videos have been downloaded
        current_video_in_download = 1
    # Get the quality of the video streams selected by the user from a drop-down menu
        quality = self.comboBox_2.currentIndex()

    # Update the application event loop to make sure the user interface remains responsive while videos are downloading
        QApplication.processEvents()

    # Loop through each video in the playlist
        for video in playlist_videos:

            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            has_audio = False
            self.lcdNumber.display(current_video_in_download)

            for s in current_video_stream:
                if s.extension in ('.mp3', '.aac', '.ogg', '.wma', '.m4a', '.flac'):
                    has_audio = True
                    break

            if has_audio:
                self.lcdNumber.display(current_video_in_download)
                download = current_video_stream[quality].download(
                    callback=self.Playlist_Progress)
            QApplication.processEvents()

            current_video_in_download += 1
        else:
            QMessageBox.warning(
                self, "Download Error", f"{current_video.title} does not have an audio stream available.")

        QMessageBox.information(self, "Download Complete",
                                "The playlist has been downloaded successfully.")

    def Playlist_Progress(self, total, received, ratio, rate, time):
        # Store the amount of data received so far
        read_data = received
    # Calculate and display the download progress percentage
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            # Calculate and display the remaining time
            remaining_time = round(time/60, 2)
            self.label_6.setText(
                str('{} minutes remaining'.format(remaining_time)))
            # Refresh the display of the progress bar
            QApplication.processEvents()

    def Playlist_Save_Browse(self):
        # Open a file dialog to choose the download directory
        playlist_save_location = QFileDialog.getExistingDirectory(
            self, "Select Download Directory")
    # Update the display of the "Save Location" line edit, if a directory was selected
        self.lineEdit_6.setText(playlist_save_location)

    ################################################
    # UI CHanges Methods
    def Open_Home(self):
        # Switch to the tab at index 0 (home tab)
        self.tabWidget.setCurrentIndex(0)

    def Open_Youtube(self):
        # Switch to the tab at index 2 (YouTube tab)
        self.tabWidget.setCurrentIndex(1)

    def Open_Settings(self):
        # Switch to the tab at index 2 (Setting tab)
        self.tabWidget.setCurrentIndex(2)


    ###### App Themes ####
     # Define the function to apply DarkOrange style
    def Apply_DarkOrange_Style(self):
        # Read the contents of the darkorange.css file and store them in the 'style' variable
        style = open('themes/darkorange.css', 'r')
        style = style.read()
    # Set the style sheet of the main window to the contents of the 'style' variable
        self.setStyleSheet(style)

     # Define the function to apply QDark style
    def Apply_QDark_Style(self):
        # Read the contents of the qdark.css file and store them in the 'style' variable
        style = open('themes/qdark.css', 'r')
        style = style.read()
    # Set the style sheet of the main window to the contents of the 'style' variable
        self.setStyleSheet(style)

     # Define the function to apply DarkGray style
    def Apply_DarkGray_Style(self):
        # Read the contents of the qdarkgray.css file and store them in the 'style' variable
        style = open('themes/qdarkgray.css', 'r')
        style = style.read()
    # Set the style sheet of the main window to the contents of the 'style' variable
        self.setStyleSheet(style)

     # Define the function to apply QDarkBlue style
    def Apply_QDarkBlue_Style(self):
        # Read the contents of the darkblu.css file and store them in the 'style' variable
        style = open('themes/darkblu.css', 'r')
        style = style.read()
    # Set the style sheet of the main window to the contents of the 'style' variable
        self.setStyleSheet(style)

    ##########################################
    # App Animation
    def Move_Box_2(self):
        # Create a QPropertyAnimation object to animate the geometry property of self.groupBox_2
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation2.setDuration(2500)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(210, 50, 281, 141))
        box_animation2.start()
        self.box_animation2 = box_animation2
     # Define the function to move Box 3

    def Move_Box_3(self):
        # Create a QPropertyAnimation object to animate the geometry property of self.groupBox_3
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(2500)
        box_animation3.setStartValue(QRect(0, 0, 0, 0))
        box_animation3.setEndValue(QRect(60, 210, 281, 141))
        box_animation3.start()
        self.box_animation3 = box_animation3
     # Define the function to move Box 4

    def Move_Box_4(self):
        # Create a QPropertyAnimation object to animate the geometry property of self.groupBox_4
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation4.setDuration(2500)
        box_animation4.setStartValue(QRect(0, 0, 0, 0))
        box_animation4.setEndValue(QRect(380, 210, 281, 141))
        box_animation4.start()
        self.box_animation4 = box_animation4
        #########################################
    def apply_settings(self):
        print("Applying settings")
        # Code to apply the selected settings

    def save_settings(self):
        print("Saving settings")
        # Code to save the selected settings

    def restore_defaults(self):
        print("Restoring default settings")
        # Code to restore the default settings

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit',
                                     "Are you sure you want to exit?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def QtWidgetsQLineEdit(self):
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_7 = QtWidgets.QLineEdit(self)
        



def main():
        # Create a QApplication object and pass in a list of command-line arguments
        app = QApplication(sys.argv)
        # Create an instance of the MainApp class, which represents the main window of the app
        window = MainApp()
        # Show the main window
        window.show()
        # Start the event loop of the application
        app.exec()


    # If the script is being run as the main program, call the main() function
if __name__ == '__main__':
        main()
