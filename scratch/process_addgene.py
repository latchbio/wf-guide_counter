"""Turn addgene library .txt file to CSV conducive to guide-counter ingestion."""

import csv

with open("brie.csv", "w") as csvf:
    writer = csv.DictWriter(csvf, fieldnames=["id", "guide_seq", "gene"])
    writer.writeheader()

    # File as downloaded from
    # https://www.addgene.org/pooled-library/broadgpp-mouse-knockout-brie/.
    with open("broadgpp-brie-library-contents.txt") as f:
        for line in f.readlines():
            sl = line.split()
            writer.writerow(
                {
                    "id": f"{sl[1]}_{sl[2]}_{sl[4]}_{sl[5]}",
                    "guide_seq": sl[6],
                    "gene": sl[1],
                }
            )
