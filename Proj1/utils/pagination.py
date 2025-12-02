def paginate(items, page=1, page_size=10, title="TRACKS"):
    if not items:
        print("\nNo items available.")
        return

    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size

    # keep page in bounds
    page = max(1, min(page, total_pages))

    start = (page - 1) * page_size
    end = start + page_size

    print(f"\n===== {title} (Page {page}/{total_pages}) =====\n")

    for i, item in enumerate(items[start:end], start=start + 1):

    # ✅ PLAYLIST (has "name" and "tracks")
        if isinstance(item, dict) and "name" in item and "tracks" in item:
            name = item["name"]
            track_count = len(item["tracks"])

            print(f"{i}. {name}  ({track_count} tracks)")

        # ✅ TRACK stored as dict
        elif isinstance(item, dict):
            title = item.get("title", "Unknown")
            artist = item.get("artist", "Unknown")
            duration = item.get("duration", "00:00")

            print(f"{i}. {title} – {artist} ({duration})")

        # ✅ TRACK stored as object
        else:
            title = getattr(item, "title", "Unknown")
            artist = getattr(item, "artist", "Unknown")
            duration = getattr(item, "duration", "00:00")

            print(f"{i}. {title} – {artist} ({duration})")

    print("\n[n] Next page  \n[p] Previous page \n[b] Back")
