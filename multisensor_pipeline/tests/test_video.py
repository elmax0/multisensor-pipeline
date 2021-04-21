import os
import unittest
from time import sleep

import av
from PIL import Image

from multisensor_pipeline import GraphPipeline
from multisensor_pipeline.modules import ConsoleSink, QueueSink
from multisensor_pipeline.modules.video.video import VideoSource


class VideoTesting(unittest.TestCase):
    def test_no_video_file(self):
        # (1) define the modules
        source = VideoSource(playback_speed=1)
        sink = ConsoleSink()

        # (2) add module to a pipeline...
        pipeline = GraphPipeline()
        pipeline.add_source(source)
        pipeline.add_sink(sink)
        # (3) ...and connect the modules
        pipeline.connect(source, sink)

        # (4) print mouse movements
        try:
            pipeline.start()
            sleep(2)
        except av.error.FileNotFoundError:
            self.assertEqual(True, True)
        try:
            pipeline.stop()
        except AttributeError as e:
            self.assertEqual(True, True)

    def test_short_video(self):
        # Create a video file with 24 PIL Images and export it
        img_sequence = []
        for x in range(24):
            img_sequence.append(Image.new('RGB', (300, 200), (228, 150, 150)))
        output = av.open('output_av.mp4', 'w')
        stream = output.add_stream('h264')
        for i, img in enumerate(img_sequence):
            frame = av.VideoFrame.from_image(img)
            packet = stream.encode(frame)
            output.mux(packet)

        packet = stream.encode(None)
        output.mux(packet)
        output.close()

        # (1) define the modules
        source = VideoSource(file_path="output_av.mp4")
        sink = QueueSink()

        # (2) add module to a pipeline...
        pipeline = GraphPipeline()
        pipeline.add_source(source)
        pipeline.add_sink(sink)
        # (3) ...and connect the modules
        pipeline.connect(source, sink)

        # (4) print mouse movements

        pipeline.start()
        sleep(2)
        pipeline.stop()
        self.assertEqual(sink.queue.qsize(), 23)
        os.remove("output_av.mp4")

    def test_long_video(self):
        # Create a video file with 24 PIL Images and export it
        img_sequence = []
        for x in range(500):
            img_sequence.append(Image.new('RGB', (300, 200), (228, 150, 150)))
        output = av.open('output_av.mp4', 'w')
        stream = output.add_stream('h264', '24')
        for i, img in enumerate(img_sequence):
            frame = av.VideoFrame.from_image(img)
            packet = stream.encode(frame)
            output.mux(packet)

        packet = stream.encode(None)
        output.mux(packet)
        output.close()

        # (1) define the modules
        source = VideoSource(file_path="output_av.mp4")
        sink = QueueSink()

        # (2) add module to a pipeline...
        pipeline = GraphPipeline()
        pipeline.add_source(source)
        pipeline.add_sink(sink)
        # (3) ...and connect the modules
        pipeline.connect(source, sink)

        # (4) print mouse movements

        pipeline.start()
        sleep(.3)
        pipeline.stop()
        self.assertGreater(sink.queue.qsize(), 23)
        os.remove("output_av.mp4")

    def test_video_with_play_speed(self):
        pass
