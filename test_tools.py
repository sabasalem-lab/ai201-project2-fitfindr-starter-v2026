from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import load_listings, get_example_wardrobe

print("=== search_listings ===")
results = search_listings('graphic tee', max_price=30)
print(f"Found {len(results)} result(s)")
for r in results:
    print(f"  - {r['title']} (${r['price']})")

print("\n=== suggest_outfit ===")
listing = load_listings()[0]
outfit = suggest_outfit(listing, get_example_wardrobe())
print(outfit)

print("\n=== create_fit_card ===")
card = create_fit_card(outfit, listing)
print(card)