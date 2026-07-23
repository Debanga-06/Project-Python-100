import random
import pandas as pd

random.seed(7)

POSITIVE_FRAGMENTS = [
    "I absolutely loved this {noun}, it exceeded every expectation.",
    "This {noun} was fantastic from start to finish.",
    "Honestly one of the best {noun}s I've come across in a long time.",
    "Great {noun}, would recommend to anyone without hesitation.",
    "The {noun} blew me away, everything about it felt top notch.",
    "Really impressed with this {noun}, worth every penny.",
    "Such a pleasant experience with this {noun}, I'm coming back for more.",
    "This {noun} made my day, genuinely wonderful.",
    "Five stars, the {noun} was excellent and delivered on its promise.",
    "I can't stop recommending this {noun} to friends and family.",
    "Superb quality, the {noun} felt carefully made and thoughtful.",
    "What a fantastic {noun}, it just works and works well.",
    "Can't believe how good this turned out, best decision I made all week.",
    "So glad I gave this a shot, it made everything so much easier.",
    "Best purchase I've made in ages, I use it every single day now.",
    "Everything about this exceeded what I was hoping for, no complaints at all.",
    "Went above and beyond what I expected, genuinely happy with how this went.",
    "I'm thrilled with how this turned out, couldn't ask for more honestly.",
    "This made my week, everything felt smooth and well thought out.",
    "Ended up loving every bit of this, will definitely be back for more.",
    "Couldn't have asked for a better experience, staff and quality were amazing.",
    "This was a joy to use from the very first minute, highly recommend.",
    "Really happy I took the chance on this, exceeded all my expectations.",
    "Brilliant from beginning to end, one of my favorite experiences this year.",
]

NEGATIVE_FRAGMENTS = [
    "I was really disappointed with this {noun}, wouldn't buy again.",
    "This {noun} fell apart within a week, total waste of money.",
    "Awful experience, the {noun} didn't work as advertised at all.",
    "The {noun} was mediocre at best, nothing special about it.",
    "Terrible {noun}, I regret ever purchasing it.",
    "Not worth the price, the {noun} is poorly made.",
    "I had high hopes but the {noun} let me down badly.",
    "Would not recommend this {noun} to anyone, complete letdown.",
    "The {noun} broke almost immediately, very frustrating.",
    "Waste of time and money, this {noun} was a huge disappointment.",
    "Poor quality control, the {noun} arrived damaged and unusable.",
    "One star, the {noun} simply doesn't do what it claims.",
    "Everything went wrong from the start, honestly regret the whole thing.",
    "Such a letdown, expected way more and got almost nothing in return.",
    "Never again, this was hands down one of my worst experiences this year.",
    "Nothing worked the way it should have, I ended up frustrated the whole time.",
    "Completely underwhelmed, the whole thing felt rushed and cheaply put together.",
    "I want my money back, this was a total disaster from beginning to end.",
    "Kept having issue after issue, support was no help whatsoever either.",
    "Fell short in every way imaginable, wouldn't wish this on anyone.",
    "Broke down almost right away and nobody seemed to care about fixing it.",
    "Left feeling annoyed and cheated, definitely steering clear from now on.",
    "Painfully slow and clunky, honestly a headache to deal with.",
    "Everything felt cheap and rushed, deeply disappointing given the price.",
]

NEUTRAL_FRAGMENTS = [
    "The {noun} was okay, nothing more nothing less.",
    "It's an average {noun}, does the job but nothing exciting.",
    "The {noun} arrived on time, packaging was standard.",
    "Not bad, not great - the {noun} is just fine for the price.",
    "The {noun} works as described, no complaints but no praise either.",
    "It's a fairly ordinary {noun}, similar to others in this category.",
    "The {noun} does what it's supposed to, nothing stood out.",
    "Middle of the road {noun}, I have mixed feelings about it.",
    "The {noun} is functional but there's nothing memorable about it.",
    "Neither impressed nor disappointed by this {noun}.",
    "It does the job, though I probably wouldn't go out of my way for it again.",
    "Some parts were good, some were a bit lacking, evens out overall.",
    "Pretty standard experience overall, nothing that really stood out either way.",
    "It arrived as expected, works fine, just didn't leave much of an impression.",
    "Reasonable for what it is, though there's plenty of room to improve.",
    "A mixed bag honestly, some things worked well and others didn't.",
    "Got the job done without any drama, but nothing to write home about.",
    "Average at best, wouldn't go out of my way to try it again soon.",
    "It's fine for casual use, though I wouldn't call it exceptional by any means.",
    "Somewhere in the middle for me, has its ups and downs like most things.",
]

NOUNS = [
    "product", "movie", "restaurant", "app", "service", "book", "gadget",
    "hotel", "phone", "laptop", "course", "game", "show", "album",
    "delivery", "software", "camera", "headphones", "vacation", "meal"
]

INTENSIFIERS = ["", "honestly, ", "to be fair, ", "overall, ", "in my opinion, "]


def build_dataset(n_per_class=350):
    rows = []
    for fragments, label in [
        (POSITIVE_FRAGMENTS, "positive"),
        (NEGATIVE_FRAGMENTS, "negative"),
        (NEUTRAL_FRAGMENTS, "neutral"),
    ]:
        for _ in range(n_per_class):
            template = random.choice(fragments)
            noun = random.choice(NOUNS)
            intensifier = random.choice(INTENSIFIERS)
            text = intensifier + template.format(noun=noun)
            text = text[0].upper() + text[1:]
            rows.append({"text": text, "sentiment": label})

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=7).reset_index(drop=True)  # shuffle
    return df


if __name__ == "__main__":
    df = build_dataset(n_per_class=350)
    df.to_csv("data/reviews.csv", index=False)
    print(f"Wrote {len(df)} labeled reviews to data/reviews.csv")
    print(df["sentiment"].value_counts())
