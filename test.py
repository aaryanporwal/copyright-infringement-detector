import os
import ihash

def test_hamming_distance():
    assert ihash.hamming_distance("123456", "223456") == 1

def test_collage_dir():
    assert os.path.exists("frames-v2") == True

def test_video_exists():
    assert os.path.exists("video.mp4") == True

def test_collage_image():
    assert os.path.exists(os.path.join("frames-v2", "collage.jpg")) == True

def test_all():
    test_hamming_distance()
    test_collage_dir()
    test_video_exists()
    
