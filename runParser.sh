rm *.dat
touch items.dat
touch users.dat
touch bids.dat
touch ItemCategory.dat
python3 parser.py ebay_data/items-*.json
