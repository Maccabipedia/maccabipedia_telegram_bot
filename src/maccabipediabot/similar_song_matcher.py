import html
import logging

from maccabistats.parse.maccabipedia.maccabipedia_cargo_chunks_crawler import MaccabiPediaCargoChunksCrawler

from maccabipediabot.maccabi_games import _get_similar_names

_logger = logging.getLogger(__name__)
_MACCABIPEDIA_SONGS = None


def _unescape(name):
    return html.unescape(html.unescape(name))


def _fetch_songs_from_maccabipedia():
    """
    :rtype: dict[str, MaccabiPediaSong]
    """
    _logger.info("Fetching songs from maccabipedia")
    songs_from_maccabipedia = dict()
    songs = MaccabiPediaCargoChunksCrawler(tables_name="Original_Songs_Catalog",
                                           tables_fields="_pageName, SongName, OriginalSongName, Lyrics")
    for song in songs:
        songs_from_maccabipedia[_unescape(song['_pageName'])] = MaccabiPediaSong(song['_pageName'], song['SongName'],
                                                                                 song['OriginalSongName'],
                                                                                 song['Lyrics'])

    _logger.info(f"Fetched {len(songs_from_maccabipedia)} from maccabipedia")
    return songs_from_maccabipedia


def song_exists_on_maccabipedia(song_name):
    """
    Check whether this song exists on maccabipedia by its name (which lead to page_name)
    :type song_name: str
    :rtype: bool
    """
    # The page_name of the songs is without the namespace prefix
    return song_name in [song.page_name for song in get_maccabipedia_songs().values()]


def get_maccabipedia_songs():
    """
    :rtype: dict[str, MaccabiPediaSong]
    """
    global _MACCABIPEDIA_SONGS

    if _MACCABIPEDIA_SONGS is None:
        _MACCABIPEDIA_SONGS = _fetch_songs_from_maccabipedia()

    return _MACCABIPEDIA_SONGS


class MaccabiPediaSong(object):

    def __init__(self, page_name, song_name, original_song_name, lyrics):
        """
        Some of the input may be html escaped, we unescaped it
        :type page_name: str
        :type song_name: str
        :type original_song_name: str
        :type lyrics: str
        """

        self.page_name = _unescape(page_name).replace("שיר:", "")  # Remove the song namespace prefix
        self.song_name = _unescape(song_name)
        self.original_song_name = _unescape(original_song_name)
        self.lyrics = _unescape(lyrics)

    def __repr__(self):
        return f"{self.song_name}: {self.original_song_name}"


class SimilarMaccabiPediaSong(object):

    def __init__(self, search_song_by_this):
        """
        :type search_song_by_this: str
        """
        self.search_song_by_this = search_song_by_this

    def find_most_similar_songs(self):
        """
        Finds similar songs by what we can (song name, original song name and the lyrics), Returns list of page names (of the similar songs).
        :rtype: list of str
        """
        maccabipedia_songs = get_maccabipedia_songs()

        similar_songs_by_name = _get_similar_names(self.search_song_by_this,
                                                   [song.song_name for song in maccabipedia_songs.values()])
        similar_song_by_original_song = _get_similar_names(self.search_song_by_this,
                                                           [song.original_song_name for song in
                                                            maccabipedia_songs.values()])
        songs_by_lyrics = [song for song in maccabipedia_songs.values() if self.search_song_by_this in song.lyrics]

        # Add all similar songs
        similar_songs = set()
        similar_songs.update([song for song in maccabipedia_songs.values() if song.song_name in similar_songs_by_name])
        similar_songs.update(
            [song for song in maccabipedia_songs.values() if song.original_song_name in similar_song_by_original_song])
        similar_songs.update(songs_by_lyrics)

        # We want to remove the song namespace prefix so the user wont see it as recommendation
        return [song.page_name.replace("שיר:", "") for song in similar_songs]
