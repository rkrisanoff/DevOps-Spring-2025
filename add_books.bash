#!/usr/bin/env bash
set -euo pipefail

#######################################
# Параметры подключения               #
#######################################
HOST="${HOST:-localhost}"
PORT="${PORT:-8000}"
BASE_URL="http://${HOST}:${PORT}"



# ======================================
# Добавляем первые 20 книг с разными статусами
# ======================================


http POST "${BASE_URL}/api/books" \
  title="To Kill a Mockingbird" \
  author="Harper Lee" \
  genres:='["fiction","historical_fiction"]' \
  year=1960 \
  language="english" \
  pages=281 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Girl with the Dragon Tattoo" \
  author="Stieg Larsson" \
  genres:='["mystery","crime_fiction","thriller"]' \
  year=2005 \
  language="swedish" \
  pages=465 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Gone Girl" \
  author="Gillian Flynn" \
  genres:='["mystery","thriller"]' \
  year=2012 \
  language="english" \
  pages=422 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Shining" \
  author="Stephen King" \
  genres:='["horror","fiction"]' \
  year=1977 \
  language="english" \
  pages=659 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Educated" \
  author="Tara Westover" \
  genres:='["memoir","nonfiction"]' \
  year=2018 \
  language="english" \
  pages=334 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Becoming" \
  author="Michelle Obama" \
  genres:='["memoir","biography"]' \
  year=2018 \
  language="english" \
  pages=448 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Road" \
  author="Cormac McCarthy" \
  genres:='["fiction","adventure"]' \
  year=2006 \
  language="english" \
  pages=287 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Fault in Our Stars" \
  author="John Green" \
  genres:='["young_adult","romance"]' \
  year=2012 \
  language="english" \
  pages=313 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="The Chronicles of Narnia" \
  author="C. S. Lewis" \
  genres:='["fantasy","childrens"]' \
  year=1956 \
  language="english" \
  pages=767 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Kite Runner" \
  author="Khaled Hosseini" \
  genres:='["historical_fiction","fiction"]' \
  year=2003 \
  language="english" \
  pages=371 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="A Brief History of Time" \
  author="Stephen Hawking" \
  genres:='["nonfiction","history"]' \
  year=1988 \
  language="english" \
  pages=212 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="The Art of War" \
  author="Sun Tzu" \
  genres:='["philosophy","history"]' \
  year=-500 \
  language="chinese" \
  pages=64 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="Les Misérables" \
  author="Victor Hugo" \
  genres:='["historical_fiction","fiction"]' \
  year=1862 \
  language="french" \
  pages=1463 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Don Quixote" \
  author="Miguel de Cervantes" \
  genres:='["adventure","historical_fiction"]' \
  year=1605 \
  language="spanish" \
  pages=863 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="War and Peace" \
  author="Leo Tolstoy" \
  genres:='["historical_fiction","fiction"]' \
  year=1869 \
  language="russian" \
  pages=1225 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Divine Comedy" \
  author="Dante Alighieri" \
  genres:='["poetry","historical_fiction"]' \
  year=1320 \
  language="italian" \
  pages=798 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Inferno" \
  author="Dan Brown" \
  genres:='["mystery","thriller"]' \
  year=2013 \
  language="english" \
  pages=480 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Watchmen" \
  author="Alan Moore" \
  genres:='["graphic_novel","fiction"]' \
  year=1987 \
  language="english" \
  pages=416 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Little Prince" \
  author="Antoine de Saint-Exupéry" \
  genres:='["childrens","philosophy"]' \
  year=1943 \
  language="french" \
  pages=96 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Da Vinci Code" \
  author="Dan Brown" \
  genres:='["mystery","thriller"]' \
  year=2003 \
  language="english" \
  pages=689 \
  status="todo"

# ======================================
# Добавляем ещё 30 книг
# ======================================

http POST "${BASE_URL}/api/books" \
  title="Moby-Dick" \
  author="Herman Melville" \
  genres:='["fiction","adventure"]' \
  year=1851 \
  language="english" \
  pages=585 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="Pride and Prejudice" \
  author="Jane Austen" \
  genres:='["romance","historical_fiction"]' \
  year=1813 \
  language="english" \
  pages=432 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Ulysses" \
  author="James Joyce" \
  genres:='["fiction","philosophy"]' \
  year=1922 \
  language="english" \
  pages=730 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Anna Karenina" \
  author="Leo Tolstoy" \
  genres:='["fiction","historical_fiction"]' \
  year=1877 \
  language="russian" \
  pages=864 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Odyssey" \
  author="Homer" \
  genres:='["poetry","history"]' \
  year=-800 \
  language="greek" \
  pages=541 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="One Hundred Years of Solitude" \
  author="Gabriel García Márquez" \
  genres:='["fiction","historical_fiction"]' \
  year=1967 \
  language="spanish" \
  pages=417 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Brothers Karamazov" \
  author="Fyodor Dostoevsky" \
  genres:='["philosophy","fiction"]' \
  year=1880 \
  language="russian" \
  pages=824 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="Madame Bovary" \
  author="Gustave Flaubert" \
  genres:='["fiction","historical_fiction"]' \
  year=1856 \
  language="french" \
  pages=328 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="The Stranger" \
  author="Albert Camus" \
  genres:='["fiction","philosophy"]' \
  year=1942 \
  language="french" \
  pages=123 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Beloved" \
  author="Toni Morrison" \
  genres:='["fiction","historical_fiction"]' \
  year=1987 \
  language="english" \
  pages=324 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Catcher in the Rye" \
  author="J. D. Salinger" \
  genres:='["fiction","young_adult"]' \
  year=1951 \
  language="english" \
  pages=277 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Frankenstein" \
  author="Mary Shelley" \
  genres:='["horror","science_fiction"]' \
  year=1818 \
  language="english" \
  pages=280 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Dracula" \
  author="Bram Stoker" \
  genres:='["horror","fiction"]' \
  year=1897 \
  language="english" \
  pages=418 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="Sense and Sensibility" \
  author="Jane Austen" \
  genres:='["romance","historical_fiction"]' \
  year=1811 \
  language="english" \
  pages=226 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Iliad" \
  author="Homer" \
  genres:='["poetry","history"]' \
  year=-750 \
  language="greek" \
  pages=683 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Count of Monte Cristo" \
  author="Alexandre Dumas" \
  genres:='["adventure","fiction"]' \
  year=1844 \
  language="french" \
  pages=1276 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Les Fleurs du mal" \
  author="Charles Baudelaire" \
  genres:='["poetry"]' \
  year=1857 \
  language="french" \
  pages=300 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Sun Also Rises" \
  author="Ernest Hemingway" \
  genres:='["fiction","adventure"]' \
  year=1926 \
  language="english" \
  pages=251 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Old Man and the Sea" \
  author="Ernest Hemingway" \
  genres:='["fiction"]' \
  year=1952 \
  language="english" \
  pages=127 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="Lolita" \
  author="Vladimir Nabokov" \
  genres:='["fiction","philosophy"]' \
  year=1955 \
  language="english" \
  pages=336 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Sound and the Fury" \
  author="William Faulkner" \
  genres:='["fiction"]' \
  year=1929 \
  language="english" \
  pages=326 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Invisible Man" \
  author="Ralph Ellison" \
  genres:='["fiction","philosophy"]' \
  year=1952 \
  language="english" \
  pages=581 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="On the Road" \
  author="Jack Kerouac" \
  genres:='["adventure","fiction"]' \
  year=1957 \
  language="english" \
  pages=320 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Memoirs of a Geisha" \
  author="Arthur Golden" \
  genres:='["historical_fiction","memoir"]' \
  year=1997 \
  language="english" \
  pages=448 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Handmaid's Tale" \
  author="Margaret Atwood" \
  genres:='["science_fiction","fiction"]' \
  year=1985 \
  language="english" \
  pages=311 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="The Color Purple" \
  author="Alice Walker" \
  genres:='["fiction","memoir"]' \
  year=1982 \
  language="english" \
  pages=295 \
  status="todo"

http POST "${BASE_URL}/api/books" \
  title="Midnight's Children" \
  author="Salman Rushdie" \
  genres:='["fiction","historical_fiction"]' \
  year=1981 \
  language="english" \
  pages=529 \
  status="reading"

http POST "${BASE_URL}/api/books" \
  title="One Day in the Life of Ivan Denisovich" \
  author="Aleksandr Solzhenitsyn" \
  genres:='["historical_fiction","fiction"]' \
  year=1962 \
  language="russian" \
  pages=165 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="Things Fall Apart" \
  author="Chinua Achebe" \
  genres:='["historical_fiction","fiction"]' \
  year=1958 \
  language="english" \
  pages=209 \
  status="finished"

http POST "${BASE_URL}/api/books" \
  title="The Alchemist" \
  author="Paulo Coelho" \
  genres:='["fiction","philosophy"]' \
  year=1988 \
  language="portuguese" \
  pages=208 \
  status="reading"
