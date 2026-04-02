
"""
╔══════════════════════════════════════════════════════════════════╗
║         FACIAL RECOGNITION SYSTEM — Advanced CV Pipeline        ║
║     OpenCV · Deep Learning · FaceNet · Anti-Spoofing · Logs     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import argparse
import warnings
warnings.filterwarnings('ignore')

from core.recognizer   import FacialRecognizer
from core.trainer      import FaceTrainer
from core.detector     import FaceDetector
from core.anti_spoof   import AntiSpoofing
from core.database     import FaceDatabase
from core.visualizer   import Visualizer
from core.logger       import SystemLogger
from config            import Config


def parse_args():
    parser = argparse.ArgumentParser(description="Advanced Facial Recognition System")
    sub    = parser.add_subparsers(dest="command")

    # register
    reg = sub.add_parser("register", help="Register a new face")
    reg.add_argument("--name",   required=True,  help="Person's name")
    reg.add_argument("--source", default="0",    help="Camera index or image folder path")
    reg.add_argument("--samples",type=int, default=30, help="Number of face samples to capture")

    # train
    sub.add_parser("train", help="Train recognizer on registered faces")

    # recognize
    rec = sub.add_parser("recognize", help="Real-time recognition")
    rec.add_argument("--source",  default="0",    help="Camera index or video file")
    rec.add_argument("--spoof",   action="store_true", help="Enable anti-spoofing")
    rec.add_argument("--save",    action="store_true", help="Save output video")

    # analyze
    ana = sub.add_parser("analyze", help="Analyze an image or video file")
    ana.add_argument("--input",   required=True,  help="Path to image or video")
    ana.add_argument("--output",  default=None,   help="Output path")

    # stats
    sub.add_parser("stats", help="Show database & recognition statistics")

    return parser.parse_args()


def main():
    args = parse_args()
    cfg  = Config()
    log  = SystemLogger(cfg)

    print(f"\n{'='*65}")
    print(f"  🎯 Facial Recognition System")
    print(f"  Command : {args.command or 'help'}")
    print(f"{'='*65}\n")

    if args.command == "register":
        db      = FaceDatabase(cfg)
        det     = FaceDetector(cfg)
        trainer = FaceTrainer(cfg, db, det, log)
        trainer.register(args.name, args.source, args.samples)

    elif args.command == "train":
        db      = FaceDatabase(cfg)
        det     = FaceDetector(cfg)
        trainer = FaceTrainer(cfg, db, det, log)
        trainer.train()

    elif args.command == "recognize":
        db      = FaceDatabase(cfg)
        det     = FaceDetector(cfg)
        spoof   = AntiSpoofing(cfg) if args.spoof else None
        rec     = FacialRecognizer(cfg, db, det, spoof, log)
        rec.run_realtime(args.source, save=args.save)

    elif args.command == "analyze":
        db      = FaceDatabase(cfg)
        det     = FaceDetector(cfg)
        rec     = FacialRecognizer(cfg, db, det, None, log)
        viz     = Visualizer(cfg)
        rec.analyze_file(args.input, args.output, viz)

    elif args.command == "stats":
        db  = FaceDatabase(cfg)
        viz = Visualizer(cfg)
        viz.show_stats(db)

    else:
        print("  Usage examples:")
        print("    python main.py register --name 'John Doe' --samples 40")
        print("    python main.py train")
        print("    python main.py recognize --source 0 --spoof")
        print("    python main.py analyze --input photo.jpg")
        print("    python main.py stats\n")


if __name__ == "__main__":
    main()