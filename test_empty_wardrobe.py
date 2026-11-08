from agent import run_agent
from utils.data_loader import get_empty_wardrobe

session = run_agent(
    query="looking for a vintage graphic tee under $30",
    wardrobe=get_empty_wardrobe(),
)
print("error:", session["error"])
print("outfit_suggestion:", session["outfit_suggestion"])
print("fit_card:", session["fit_card"])