"""Base Classes for the API."""

from .partial import PartialAnime, PartialManga, PartialPerson, PartialCharacter
from .utils import parse_id, create_relation


class Anime:
    """Represents a MAL Anime

    Attributes
    ----------
    id : int
        The Anime's ID.

    title : str
        The Series title.

    type : str
       The Anime's type. Can be `ONA`/`OVA`/`TV`/`Movie`.

    synonyms : list[str]
       Alternative names for the Anime.

    image : str
        The cover image URL for the Anime.

    japanese_title : str
        Japanese title of the Anime.

    status : str
        Airing status of the Manga.

    episodes : int
        Episode count of the Manga.

    air_start : str
        Airing start date.

    air_end : str
        Airing end date.

    airing : bool
        True if the Anime is airing, False if not.

    synopsis : str
        Description of the Anime.

    producers : list[list]
        WIP - List of the Anime's producers.

    licensors : list[list]
        WIP - List of the Anime's licensors.

    studios : list[list]
        WIP - List of the Anime's studios

    premiered : str
        Premier season.

    broadcast : str
        Broadcast times.

    genres : list[str]
        List of the Anime's genres.

    link : str
        Link to the Anime on MAL.

    score : tuple(int)
        Tuple of (score, voters).

    duration : str
        Duration of the Anime (may be per episode).

    rank : int
        Anime's rank on the MAL board.

    popularity : int
        Popularity rank of the Anime.

    members : int
        Amount of members which have the Anime in their list.

    favorites : int
        Amount of favorites given to the Anime.

    source : str
        Type of source material. Can be `Manga` `Novel` or `Original`.

    related : list[:class:`.PartialAnime` or :class:`.PartialManga`]
        List of related Anime or Manga.

    """

    def __init__(self, anime_id, **kwargs):
        self.id = anime_id
        self.title = kwargs.pop('title', None)
        self.type = kwargs.pop('type', None)
        self.synonyms = kwargs.pop('title_synonyms', None)
        self.image = kwargs.pop('image_url', None)
        self.japanese_title = kwargs.pop('title_japanese', None)
        self.status = kwargs.pop('status', None)
        self.episodes = kwargs.pop('episodes', None)
        self.airing = kwargs.pop('airing', None)

        self._air_time = kwargs.pop('aired_string', None)
        if " to " not in self._air_time:
            self.air_start = self._air_time
            self.air_end = None
        else:
            self.air_start, self.air_end = self._air_time.split(" to ")

        self.premiered = kwargs.pop('premiered', None)
        self.broadcast = kwargs.pop('broadcast', None)
        self.synopsis = kwargs.pop('synopsis', None)
        self.producers = kwargs.pop('producer', None)
        self.licensors = kwargs.pop('licensor', None)
        self.studios = kwargs.pop('studio', None)
        self.source = kwargs.pop('source', None)

        self._raw_genres = kwargs.pop('genre', None)
        if self._raw_genres is None:
            self._raw_genres = kwargs.pop('genres', None)
        self.genres = [g['name'] for g in self._raw_genres] if self._raw_genres else None

        self.duration = kwargs.pop('duration', None)
        self.link = kwargs.pop('link_canonical', None)
        self.rating = kwargs.pop('rating', None)
        self.score = kwargs.pop('score', None)
        self.rank = kwargs.pop('rank', None)
        self.popularity = kwargs.pop('popularity', None)
        self.members = kwargs.pop('members', None)
        self.favorites = kwargs.pop('favorites', None)

        self.related = []
        self._raw_related = kwargs.pop('related', None)
        for relation_type, relations in self._raw_related.items():
            for relation in relations:
                relation['relation'] = relation_type
                obj = create_relation(relation)
                self.related.append(obj)


class Manga:
    """Represents a MAL Manga (Includes Novels)

    Attributes
    ----------
    id : int
        The Manga's ID.

    title : str
        The Series title.

    type : str
       The Manga's type. Can be either "Novel" or "Manga".

    synonyms : list[str]
       Alternative names for the Manga.

    image : str
        The cover image URL for the Manga.

    japanese_title : str
        Japanese title of the Manga.

    status : str
        Publishing status of the Manga.

    volumes : int
        Volume count of the Manga.

    chapters : int
        Chapter count of the Manga.

    publish_start : str
        Publication start date.

    publish_end : str
        Publication end date.

    publishing : bool
        True if the manga is publishing, False if not.

    synopsis : str
        Description of the Manga.

    author : str
        Name of the Manga author.

    serialization : str
        The Manga's serialization.

    genres : list[str]
        List of the Manga's genres.

    link : str
        Link to the Manga on MAL.

    score : tuple(int)
        Tuple of (score, voters).

    rank : int
        Manga's rank on the MAL board.

    popularity : int
        Popularity rank of the Manga.

    members : int
        Amount of members which have the Manga in their list.

    favorites : int
        Amount of favorites given to the Manga.

    related : list[:class:`.PartialAnime` or :class:`.PartialManga`]
        List of related Anime or Manga.

    """

    def __init__(self, manga_id, **kwargs):
        self.id = manga_id
        self.title = kwargs.pop('title', None)
        self.type = kwargs.pop('type', None)
        self.synonyms = kwargs.pop('title_synonyms', None)
        self.image = kwargs.pop('image_url', None)
        self.japanese_title = kwargs.pop('title_japanese', None)
        self.status = kwargs.pop('status', None)
        self.volumes = kwargs.pop('volumes', None)
        self.chapters = kwargs.pop('chapters', None)
        self.publishing = kwargs.pop('publishing', None)
        self.synopsis = kwargs.pop('synopsis', None)

        self._publish_time = kwargs.pop('published_string', None)
        if " to " not in self._publish_time:
            self.publish_start = self._publish_time
            self.publish_end = None
        else:
            self.publish_start, self.publish_end = self._publish_time.split(" to ")

        self._raw_author = kwargs.pop('author', None)[0]
        self._raw_author['id'] = parse_id(self._raw_author['url'])
        self.author = PartialPerson.from_author(self._raw_author)

        self._raw_genres = kwargs.pop('genre', None)
        if self._raw_genres is None:
            self._raw_genres = kwargs.pop('genres', None)
        self.genres = [g['name'] for g in self._raw_genres] if self._raw_genres else None

        self.serialization = kwargs.pop('serialization', None)[0]  # TODO: add serializations
        self.link = kwargs.pop('link_canonical', None)
        self.score = kwargs.pop('score', None)
        self.rank = kwargs.pop('rank', None)
        self.popularity = kwargs.pop('popularity', None)
        self.members = kwargs.pop('members', None)
        self.favorites = kwargs.pop('favorites', None)

        self.related = []
        self._raw_related = kwargs.pop('related', None)
        for relation_type, relations in self._raw_related.items():
            for relation in relations:
                relation['relation'] = relation_type
                obj = create_relation(relation)
                self.related.append(obj)


class Character:
    """Represents a MAL Character

    Attributes
    ----------
    id : int
        The Character's ID.

    name : str
        Character's name.

    link : str
        Link to the Character on MAL.

    image : str
        Image URL of the Character.

    favorites : int
        Amount of favorites the Character has.

    animeography : list[:class:`PartialAnime`]
        Anime the Character is featured in.

    mangaography : list[:class:`PartialManga`]
        Manga the Character is featured in.

    japanese_name : str
        Japanese name of the character.

    about : str
        WIP - Information about the character. As of now, spoilers are unformatted and will appear.

    voice_actors : list[dict]
        WIP - List of voice actors who played this Character.

    """

    def __init__(self, char_id, **kwargs):
        self.id = char_id
        self.link = kwargs.pop('link_canonical', None)
        self.name = kwargs.pop('name', None)
        self.image = kwargs.pop('image_url', None)
        self.favorites = kwargs.pop('member_favorites', None)

        self.animeography = []
        self._raw_animeography = kwargs.pop('animeography', None)
        for anime in self._raw_animeography:
            anime['id'] = parse_id(anime['url'])
            obj = PartialAnime.from_character(anime)
            self.animeography.append(obj)

        self.mangaography = []
        self._raw_mangaography = kwargs.pop('mangaography', None)
        for manga in self._raw_mangaography:
            manga['id'] = parse_id(manga['url'])
            obj = PartialManga.from_character(manga)
            self.mangaography.append(obj)

        self.japanese_name = kwargs.pop('name_kanji', None)
        self.about = kwargs.pop('about', None)
        self.voice_actors = kwargs.pop('voice_actors', None)  # TODO: Handle


class Person:
    """Represents a MAL Person (Voice Actors, Staff, etc.)

    Attributes
    ----------
    id : int
        The Person's ID.

    name : str
        The Person's name.

    link : str
        Link to the Person on MAL.

    image : str
        Image URL of the Person.

    favorites : int
        Amount of favorites the Person has.

    anime : list[dict]
        WIP - Staff positions in Anime.

    manga : list[dict]
        WIP - Published Manga.

    more : str
        Additional info about the Person.

    website : str
        Link to the Person's website

    voice_acting : list[dict]
        WIP - List of voice acting roles the Person has.

    """

    def __init__(self, person_id, **kwargs):
        self.id = person_id
        self.link = kwargs.pop('link_canonical', None)
        self.name = kwargs.pop('name', None)
        self.image = kwargs.pop('image_url', None)
        self.favorites = kwargs.pop('member_favorites', None)
        self.anime = kwargs.pop('anime_staff_position', None)  # TODO: Handle
        self.manga = kwargs.pop('published_manga', None)  # TODO: Handle
        self.birthday = kwargs.pop('birthday', None)
        self.more = kwargs.pop('more', None)
        self.website = kwargs.pop('website', None)
        self.voice_acting = kwargs.pop('voice_acting_role', None)  # TODO: Handle
