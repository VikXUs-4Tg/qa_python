import pytest
import random

from main import BooksCollector

test_book = 'Test Title'
test_genre = 'Test Genre'
test_books = [{},{'1':'Фантастика','2':'Ужасы'}]
test_favorites_books = [[],[test_book]]
test_correct_title = ['Я','Ад','Тестирование dot com','Жизнь кота, познавшего любовь обезьяны!','Любовь, как единственный способ выживать']
test_incorrect_title = ['', 'Жизнь кота, не познавшего любовь обезьяны','Любовь, как единственный способ жить вечно','Удивительное путешествие Нильса Хольгерссона с дикими гусями по Швеции']
test_books_with_specific_genre =                                        [
    ['Комедии', {}, []                                              ],
    [test_genre, {test_book: test_genre}, []                        ],
    ['Фантастика',{'1':'Фантастика','2':'Фантастика'}, ['1','2']    ],
    ['Фантастика',{'1':'Фантастика','2':'Ужасы'}, ['1']             ],
    ['Ужасы',{'1':'Фантастика','2':'Ужасы'}, ['2']                  ],
    ['Мультфильмы',{'1':'Фантастика','2':'Ужасы'}, []               ]   ]
test_books_for_children =                                                                                           [
    [{}, []                                                                                                     ],
    [{test_book: test_genre}, []                                                                                ],
    [{'1':'Фантастика', '2': 'Мультфильмы','3': 'Комедии'}, ['1','2','3']                                       ],
    [{'1': 'Фантастика', '2': 'Мультфильмы', '3': 'Комедии', '4': 'Ужасы', '5': 'Детективы'}, ['1', '2', '3']   ],
    [{'4':'Ужасы','5':'Детективы'}, []                                                                          ]   ]
test_add_favorites_books =              [
    [{}, '1', []                    ],
    [{'1':'Фантастика'}, '2', []    ],
    [{'1':'Фантастика'}, '1', ['1'] ]   ]
test_delete_favorites_books =   [
    [['1'], '1', []         ],
    [['1','2'], '2', ['1']  ],
    [['1'], '2', ['1']      ]   ]

class TestBooksCollector:

    @pytest.mark.parametrize('book', test_correct_title)
    def test_add_new_book_correct_title_is_added(self, book):
        collector = BooksCollector()
        collector.add_new_book(book)
        assert collector.books_genre == {book:''}

    @pytest.mark.parametrize('book', test_incorrect_title)
    def test_add_new_book_incorrect_title_not_added(self, book):
        collector = BooksCollector()
        collector.add_new_book(book)
        assert collector.books_genre == {}

    def test_add_new_book_existing_book_not_added(self):
        collector = BooksCollector()
        collector.add_new_book(test_book)
        collector.add_new_book(test_book)
        assert collector.books_genre == {test_book:''}

    def test_set_book_genre_existing_title_and_genre_setting_genre(self):
        collector = BooksCollector()
        test_random_genre = random.choice(collector.genre)
        collector.add_new_book(test_book)
        collector.set_book_genre(test_book, test_random_genre)
        assert collector.books_genre == {test_book:test_random_genre}

    def test_set_book_genre_existing_title_but_not_genre_not_setting_genre(self):
        collector = BooksCollector()
        collector.add_new_book(test_book)
        collector.set_book_genre(test_book, test_genre)
        assert collector.books_genre == {test_book:''}

    def test_set_book_genre_existing_genre_but_not_title_not_setting_genre(self):
        collector = BooksCollector()
        test_random_genre = random.choice(collector.genre)
        collector.set_book_genre(test_book, test_random_genre)
        assert collector.books_genre == {}

    def test_get_book_genre_existing_title_return_book_genre(self):
        collector = BooksCollector()
        collector.books_genre = {test_book:test_genre}
        assert collector.get_book_genre(test_book) == test_genre

    def test_get_book_genre_not_existing_title_return_none(self):
        collector = BooksCollector()
        assert collector.get_book_genre(test_book) == None

    @pytest.mark.parametrize('specific_genre,books,result', test_books_with_specific_genre)
    def test_get_books_with_specific_genre_genre_and_books_return_books_with_specific_genre(self, specific_genre, books, result):
        collector = BooksCollector()
        collector.books_genre = books
        assert collector.get_books_with_specific_genre(specific_genre) == result

    @pytest.mark.parametrize('books', test_books)
    def test_get_books_genre_books_return_books_genre(self, books):
        collector = BooksCollector()
        collector.books_genre = books
        assert collector.get_books_genre() == books

    @pytest.mark.parametrize('books,result', test_books_for_children)
    def test_get_books_for_children_books_return_books_for_children(self, books, result):
        collector = BooksCollector()
        collector.books_genre = books
        assert collector.get_books_for_children() == result

    @pytest.mark.parametrize('books,favorites_book,result', test_add_favorites_books)
    def test_add_book_in_favorites_favorites_book_add_to_favorites_if_name_pass(self, books, favorites_book, result):
        collector = BooksCollector()
        collector.books_genre = books
        collector.add_book_in_favorites(favorites_book)
        assert collector.favorites == result

    def test_add_book_in_favorites_favorites_book_existing_book_not_added(self):
        collector = BooksCollector()
        test_random_genre = random.choice(collector.genre)
        collector.books_genre = {test_book:test_random_genre}
        collector.favorites = [test_book]
        collector.add_book_in_favorites(test_book)
        assert collector.favorites == [test_book]

    @pytest.mark.parametrize('favorites_books,book,result', test_delete_favorites_books)
    def test_delete_book_from_favorites_book_delete_from_favorites_if_name_pass(self, favorites_books, book, result):
        collector = BooksCollector()
        collector.favorites = favorites_books
        collector.delete_book_from_favorites(book)
        assert collector.favorites == result

    @pytest.mark.parametrize('favorites_books', test_favorites_books)
    def test_get_list_of_favorites_books_favorites_books_return_favorites_books(self, favorites_books):
        collector = BooksCollector()
        collector.favorites = favorites_books
        assert collector.get_list_of_favorites_books() == favorites_books