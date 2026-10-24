"""Protect the public deployment boundary."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(name="stage_site", location=Path(__file__).resolve().parents[1] / "tools/stage_site.py")
_STAGE = importlib.util.module_from_spec(spec=_SPEC)
_SPEC.loader.exec_module(module=_STAGE)


class StageSiteTest(unittest.TestCase):
    def test_only_public_files_are_staged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            for name in _STAGE._PUBLIC_FILES:
                (source / name).write_text(data="public")
            for name in _STAGE._PUBLIC_DIRECTORIES:
                (source / name).mkdir()
                (source / name / "index.html").write_text(data="public")
            for name in ("tools", "content", "tests", ".git", ".github"):
                (source / name).mkdir()
                (source / name / "private.txt").write_text(data="private")
            (source / "future-secret.txt").write_text(data="private")
            destination = Path(temporary) / "published"
            _STAGE.stage_site(source=source, destination=destination)
            self.assertEqual(set(path.name for path in destination.iterdir()), set((*_STAGE._PUBLIC_FILES, *_STAGE._PUBLIC_DIRECTORIES)))
            self.assertFalse(any(path.name == "private.txt" for path in destination.rglob("*")))
            self.assertEqual((destination / "practice/index.html").read_text(), "public")
            with self.assertRaises(FileExistsError):
                _STAGE.stage_site(source=source, destination=destination)

    def test_symlink_cannot_publish_a_private_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            for name in _STAGE._PUBLIC_FILES:
                (source / name).write_text(data="public")
            for name in _STAGE._PUBLIC_DIRECTORIES:
                (source / name).mkdir()
            private = Path(temporary) / "private.txt"
            private.write_text(data="private")
            (source / "assets/leak.txt").symlink_to(target=private)
            with self.assertRaises(ValueError):
                _STAGE.stage_site(source=source, destination=Path(temporary) / "published")


if __name__ == "__main__":
    unittest.main()
