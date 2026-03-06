"""
'dashboard.py'
=========================================
Creates a dashboard via API with one of each block type.

The script will:
1) Ensure at least two feeds exist in the account.
2) Ensure each feed has at least five datapoints.
3) Create a new dashboard.
4) Create one block for each supported visual type.
5) Apply a responsive layout using update_layouts.

Author(s): Doug Zobel
"""
import json
import os
import requests
from random import randrange
from Adafruit_IO import Client, Data, Feed, Block, Dashboard, Layout
from Adafruit_IO.errors import RequestError

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME', '')

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure **not** to publish it when you publish this code!
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY', '')

FEED_NAMES = [
    "Dashboard Example Sensor A",
    "Dashboard Example Sensor B",
]

MIN_DATAPOINTS_PER_FEED = 5
REQUIRED_FEED_COUNT = 2

# Set True to only prepare feeds/datapoints, then stop before dashboard creation.
FEEDS_ONLY_MODE = False

BLOCK_TYPES = [
    "toggle_button",
    "slider",
    "momentary_button",
    "gauge",
    "line_gauge",
    "line_chart",
    "text",
    "color_picker",
    "map",
    "stream",
    "image",
    "remote_control",
    "multiline_text",
    # "rich_text",  # Not in UI block picker, has template: input no preview
    # see https://io.adafruit.com/api/docs/#visual-types
    "icon",
    "indicator",
    "number_pad",
    # "selector",  # Selector (radio/dropdown) block not in UI
    "dashboard_link",
    "battery",
    "divider",
]

EXAMPLE_DASHBOARD_NAME = "Adafruit IO Python Example - All Block Types"
EXAMPLE_DASHBOARD_KEY = "api-dashboard-block-types-example"

# Optional public dashboard link target. Set these env vars to point at any
# public dashboard in another account and the dashboard_link block will use it.
PUBLIC_DASHBOARD_USERNAME = os.getenv("PUBLIC_DASHBOARD_USERNAME", "tyeth")
PUBLIC_DASHBOARD_KEY = os.getenv("PUBLIC_DASHBOARD_KEY", "2025-06-24-sliders-and-toggle")
PUBLIC_DASHBOARD_NAME = os.getenv("PUBLIC_DASHBOARD_NAME", "2025-06-24 sliders and toggle")

NON_FEED_BLOCK_TYPES = {
    "divider",
}

SECONDARY_FEED_BLOCK_TYPES = {
    "line_chart",
    "stream",
    "map",
}


def is_numeric_value(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def get_user_info(aio):
    """Call /api/v2/user for subscription/sidebar metadata."""
    response = requests.get(
        "{0}/api/v2/user".format(aio.base_url),
        headers={"X-AIO-Key": aio.key},
        proxies=aio.proxies,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_throttle_info(aio):
    """Call /api/v2/{username}/throttle for current data rate usage."""
    return aio._get("throttle")


def get_nested(data, path):
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def extract_feed_limits(user_info):
    """Extract feed limit/remaining from likely /user payload paths."""
    feed_limit_paths = [
        ("user", "subscription", "limits", "feeds"),
        ("subscription", "limits", "feeds"),
        ("user", "subscription", "limits", "feeds_count"),
        ("subscription", "limits", "feeds_count"),
    ]
    feed_remaining_paths = [
        ("sidebar", "feeds", "remaining"),
        ("user", "sidebar", "feeds", "remaining"),
        ("sidebar", "remaining_feeds"),
        ("user", "sidebar", "remaining_feeds"),
        ("user", "subscription", "limits", "feeds_remaining"),
        ("subscription", "limits", "feeds_remaining"),
    ]

    feed_limit = None
    for path in feed_limit_paths:
        feed_limit = to_int(get_nested(user_info, path))
        if feed_limit is not None:
            break

    feed_remaining = None
    for path in feed_remaining_paths:
        feed_remaining = to_int(get_nested(user_info, path))
        if feed_remaining is not None:
            break

    if feed_limit is None and feed_remaining is None:
        raise RuntimeError("Could not determine feed limits from /api/v2/user response.")

    return feed_limit, feed_remaining


def extract_dashboard_limits(user_info):
    dashboard_limit_paths = [
        ("user", "subscription", "limits", "dashboards"),
        ("subscription", "limits", "dashboards"),
        ("user", "subscription", "limits", "dashboards_count"),
        ("subscription", "limits", "dashboards_count"),
    ]
    dashboard_remaining_paths = [
        ("sidebar", "dashboards", "remaining"),
        ("user", "sidebar", "dashboards", "remaining"),
        ("sidebar", "remaining_dashboards"),
        ("user", "sidebar", "remaining_dashboards"),
        ("user", "subscription", "limits", "dashboards_remaining"),
        ("subscription", "limits", "dashboards_remaining"),
    ]

    dashboard_limit = None
    for path in dashboard_limit_paths:
        dashboard_limit = to_int(get_nested(user_info, path))
        if dashboard_limit is not None:
            break

    dashboard_remaining = None
    for path in dashboard_remaining_paths:
        dashboard_remaining = to_int(get_nested(user_info, path))
        if dashboard_remaining is not None:
            break

    if dashboard_limit is None and dashboard_remaining is None:
        raise RuntimeError("Could not determine dashboard limits from /api/v2/user response.")

    return dashboard_limit, dashboard_remaining


def extract_group_limits(user_info):
    group_limit_paths = [
        ("user", "subscription", "limits", "groups"),
        ("subscription", "limits", "groups"),
        ("user", "subscription", "limits", "groups_count"),
        ("subscription", "limits", "groups_count"),
    ]
    group_remaining_paths = [
        ("sidebar", "groups", "remaining"),
        ("user", "sidebar", "groups", "remaining"),
        ("sidebar", "remaining_groups"),
        ("user", "sidebar", "remaining_groups"),
        ("user", "subscription", "limits", "groups_remaining"),
        ("subscription", "limits", "groups_remaining"),
    ]

    group_limit = None
    for path in group_limit_paths:
        group_limit = to_int(get_nested(user_info, path))
        if group_limit is not None:
            break

    group_remaining = None
    for path in group_remaining_paths:
        group_remaining = to_int(get_nested(user_info, path))
        if group_remaining is not None:
            break

    return group_limit, group_remaining


def get_all_feeds_raw(aio):
    """Return raw feed records to inspect fields not in the Feed model."""
    return aio._get("feeds")


def get_or_create_named_feed(aio, feed_name):
    for feed in aio.feeds():
        if feed.name == feed_name:
            return feed
    return aio.create_feed(Feed(name=feed_name))


def ensure_feed_capacity_for_creation(aio, feeds_to_create):
    if feeds_to_create <= 0:
        return

    user_info = get_user_info(aio)
    feed_limit, feed_remaining = extract_feed_limits(user_info)

    if feed_remaining is not None and feed_remaining < feeds_to_create:
        raise RuntimeError(
            "Not enough feed allowance remaining: need {0}, remaining {1}.".format(
                feeds_to_create,
                feed_remaining,
            )
        )

    if feed_limit is not None:
        existing_count = len(aio.feeds())
        if existing_count + feeds_to_create > feed_limit:
            raise RuntimeError(
                "Feed limit would be exceeded: current {0}, creating {1}, limit {2}.".format(
                    existing_count,
                    feeds_to_create,
                    feed_limit,
                )
            )

    print("Feed allowance check passed for creating {0} feed(s).".format(feeds_to_create))


def ensure_dashboard_capacity_for_creation(aio, dashboards_to_create):
    if dashboards_to_create <= 0:
        return

    user_info = get_user_info(aio)
    dashboard_limit, dashboard_remaining = extract_dashboard_limits(user_info)

    if dashboard_remaining is not None and dashboard_remaining < dashboards_to_create:
        raise RuntimeError(
            "Not enough dashboard allowance remaining: need {0}, remaining {1}.".format(
                dashboards_to_create,
                dashboard_remaining,
            )
        )

    if dashboard_limit is not None:
        existing_count = len(aio.dashboards())
        if existing_count + dashboards_to_create > dashboard_limit:
            raise RuntimeError(
                "Dashboard limit would be exceeded: current {0}, creating {1}, limit {2}.".format(
                    existing_count,
                    dashboards_to_create,
                    dashboard_limit,
                )
            )

    print("Dashboard allowance check passed for creating {0} dashboard(s).".format(dashboards_to_create))


def log_account_limits_and_usage(aio):
    user_info = get_user_info(aio)
    feed_limit, feed_remaining = extract_feed_limits(user_info)
    group_limit, group_remaining = extract_group_limits(user_info)
    dashboard_limit, dashboard_remaining = extract_dashboard_limits(user_info)

    current_feeds = len(aio.feeds())
    current_groups = len(aio.groups())
    current_dashboards = len(aio.dashboards())

    if feed_limit is not None:
        feed_used = feed_limit - (feed_remaining or 0) if feed_remaining is not None else current_feeds
        if feed_remaining is None:
            feed_remaining = max(feed_limit - feed_used, 0)
    else:
        feed_used = current_feeds

    if group_limit is not None:
        group_used = group_limit - (group_remaining or 0) if group_remaining is not None else current_groups
        if group_remaining is None:
            group_remaining = max(group_limit - group_used, 0)
    else:
        group_used = current_groups

    if dashboard_limit is not None:
        dashboard_used = dashboard_limit - (dashboard_remaining or 0) if dashboard_remaining is not None else current_dashboards
        if dashboard_remaining is None:
            dashboard_remaining = max(dashboard_limit - dashboard_used, 0)
    else:
        dashboard_used = current_dashboards

    print("Account limits/usage:")
    print("  Feeds      limit={0} used={1} remaining={2}".format(
        feed_limit,
        feed_used,
        feed_remaining,
    ))
    print("  Groups     limit={0} used={1} remaining={2}".format(
        group_limit,
        group_used,
        group_remaining,
    ))
    print("  Dashboards limit={0} used={1} remaining={2}".format(
        dashboard_limit,
        dashboard_used,
        dashboard_remaining,
    ))

    try:
        throttle = get_throttle_info(aio)
        print("  Throttle   data_rate_limit={0} active_data_rate={1}".format(
            throttle.get("data_rate_limit"),
            throttle.get("active_data_rate"),
        ))
    except Exception as error:
        print("  Throttle   unavailable ({0})".format(error))


def select_usable_feeds(aio):
    """Pick feeds that are enabled and have numeric last values."""
    usable = []
    for raw_feed in get_all_feeds_raw(aio):
        if raw_feed.get("enabled") is False:
            continue
        feed_key = raw_feed.get("key")
        if not feed_key:
            continue
        if not is_numeric_value(raw_feed.get("last_value")):
            continue
        usable.append(aio.feeds(feed_key))

    return usable


def ensure_min_data(aio, feed_key, minimum_count, include_location=False):
    """Ensure a feed has at least minimum_count datapoints."""
    current_count = len(aio.data(feed_key, max_results=minimum_count))
    missing = max(0, minimum_count - current_count)

    for _ in range(missing):
        value = randrange(0, 101)
        if include_location:
            lat = 37.7700 + (randrange(-100, 101) / 10000.0)
            lon = -122.4200 + (randrange(-100, 101) / 10000.0)
            aio.create_data(feed_key, Data(value=value, lat=lat, lon=lon))
        else:
            aio.create_data(feed_key, Data(value=value))

    return current_count + missing


def make_block(
    visual_type,
    primary_feed_id,
    secondary_feed_id,
    dashboard_link_targets,
    primary_group_id=None,
    secondary_group_id=None,
):
    """Build a Block object with sensible defaults for each visual type."""
    feed_id = primary_feed_id
    if visual_type in ("line_chart", "stream", "map"):
        feed_id = secondary_feed_id

    group_id = primary_group_id
    if visual_type in ("line_chart", "stream", "map"):
        group_id = secondary_group_id

    block_feed_entry = {"feed_id": feed_id}
    if group_id is not None:
        block_feed_entry["group_id"] = group_id

    block_feeds = [block_feed_entry]
    properties = {}

    if visual_type in NON_FEED_BLOCK_TYPES:
        block_feeds = None

    if visual_type == "line_chart":
        properties = {
            "historyHours": "24",
            "gridLines": "yes",
            "yAxisLabel": "Value"
        }
    elif visual_type == "gauge":
        properties = {
            "minValue": "0",
            "maxValue": "100",
            "label": "Gauge"
        }
    elif visual_type == "slider":
        properties = {
            "min": "0",
            "max": "100",
            "step": "1",
            "label": "Slider"
        }
    elif visual_type == "toggle_button":
        properties = {
            "onText": "ON",
            "offText": "OFF",
            "onValue": "1",
            "offValue": "0"
        }
    elif visual_type == "momentary_button":
        properties = {
            "onText": "PRESS",
            "onValue": "1",
            "release": "0"
        }
    elif visual_type == "text":
        properties = {
            "label": "Text"
        }
    elif visual_type == "multiline_text":
        properties = {
            "label": "Multiline Text",
            "value": "This is some static text!\\ntest",
            "static": False,
            "preformatted": False,
            "showIcon": True,
            "icon": "certificate",
        }
    elif visual_type == "stream":
        properties = {
            "showGroupName": "yes",
            "showTimestamp": "yes"
        }
    elif visual_type == "map":
        properties = {
            "historyHours": "24",
            "showNumbers": "yes"
        }
    elif visual_type == "number_pad":
        properties = {
            "label": "Number Pad"
        }
    elif visual_type == "selector":
        properties = {
            "label": "Selector",
            "min": "0",
            "max": "100",
            "step": "50",
            "onText": "High",
            "offText": "Low",
            "onValue": "100",
            "offValue": "0",
        }
    elif visual_type == "indicator":
        properties = {
            "label": "Indicator"
        }
    elif visual_type == "icon":
        properties = {
            "icon": "dot-circle",
            "label": "Icon",
            "static": True,
            "value": "check-circle",
        }
    elif visual_type == "line_gauge":
        properties = {
            "minValue": "0",
            "maxValue": "100",
            "label": "Line Gauge"
        }
    elif visual_type == "battery":
        properties = {
            "label": "Battery"
        }
    elif visual_type == "dashboard_link":
        properties = {
            "dashboards": json.dumps(dashboard_link_targets),
        }
    elif visual_type == "divider":
        properties = {
            "label": "Section Divider"
        }
    elif visual_type == "rich_text":
        properties = {
            "text": "Dashboard API Example\nLatest value feed is connected to this block."
        }
    elif visual_type == "image":
        properties = {
            "label": "Image"
        }
    elif visual_type == "remote_control":
        properties = {
            "label": "Remote"
        }
    elif visual_type == "color_picker":
        properties = {
            "label": "Color"
        }

    return Block(
        name=visual_type.replace("_", " ").title(),
        visual_type=visual_type,
        properties=properties,
        block_feeds=block_feeds,
    )


def get_target_feed_for_block(visual_type, primary_feed, secondary_feed):
    """Return the expected feed object for a block visual type."""
    if visual_type in NON_FEED_BLOCK_TYPES:
        return None
    if visual_type in SECONDARY_FEED_BLOCK_TYPES:
        return secondary_feed
    return primary_feed


def try_patch_block_feed_binding(aio, dashboard_key, block_id, feed, group_id=None):
    """Bind a feed to an existing block using documented Replace Block payload."""
    path = "{0}/api/v2/{1}/dashboards/{2}/blocks/{3}".format(
        aio.base_url,
        aio.username,
        dashboard_key,
        block_id,
    )
    headers = {
        "X-AIO-Key": aio.key,
        "Content-Type": "application/json",
    }

    payload = {
        "block": {
            "block_feeds": [
                {
                    "feed_id": feed.id,
                    "group_id": group_id,
                }
            ]
        }
    }

    if group_id is None:
        del payload["block"]["block_feeds"][0]["group_id"]

    response = requests.put(
        path,
        headers=headers,
        proxies=aio.proxies,
        json=payload,
        timeout=30,
    )
    if response.status_code >= 400:
        return None
    return response.json()


def create_block_via_http(aio, dashboard_key, block):
    """Create a block using the documented payload wrapper: {"block": {...}}."""
    path = "{0}/api/v2/{1}/dashboards/{2}/blocks".format(
        aio.base_url,
        aio.username,
        dashboard_key,
    )
    headers = {
        "X-AIO-Key": aio.key,
        "Content-Type": "application/json",
    }

    block_payload = {
        "visual_type": block.visual_type,
        "name": block.name,
        "properties": block.properties,
    }
    if block.block_feeds is not None:
        block_payload["block_feeds"] = block.block_feeds

    response = requests.post(
        path,
        headers=headers,
        proxies=aio.proxies,
        json={"block": block_payload},
        timeout=30,
    )
    response.raise_for_status()
    return Block.from_dict(response.json())


def build_layout(entries, columns):
    """Create a simple grid layout list for update_layouts."""
    layout = []
    width = 4
    height = 3
    for index, block in enumerate(entries):
        x = (index % columns) * width
        y = (index // columns) * height
        layout.append({"x": x, "y": y, "w": width, "h": height, "i": str(block.id)})
    return layout


def find_existing_example_dashboard(aio):
    for dash in aio.dashboards():
        if dash.key == EXAMPLE_DASHBOARD_KEY:
            return dash
    return None


def clear_dashboard_blocks(aio, dashboard_key):
    for block in aio.blocks(dashboard_key):
        aio.delete_block(dashboard_key, block.id)


def get_or_create_example_dashboard(aio):
    existing = find_existing_example_dashboard(aio)
    if existing is not None:
        print("Reusing existing example dashboard '{0}'.".format(existing.key))
        clear_dashboard_blocks(aio, existing.key)
        return existing

    ensure_dashboard_capacity_for_creation(aio, 1)

    name = EXAMPLE_DASHBOARD_NAME
    try:
        return aio.create_dashboard(Dashboard(name=name, key=EXAMPLE_DASHBOARD_KEY))
    except RequestError as error:
        if "Dashboard limit reached" in str(error):
            raise RuntimeError(
                "Dashboard limit reached and reusable example dashboard '{0}' was not found.".format(
                    EXAMPLE_DASHBOARD_KEY
                )
            )
        raise


def main(aio, feeds_only=False):
    log_account_limits_and_usage(aio)

    # Feed operations in this script use feed keys.
    feeds = select_usable_feeds(aio)

    if len(feeds) < REQUIRED_FEED_COUNT:
        needed = REQUIRED_FEED_COUNT - len(feeds)
        ensure_feed_capacity_for_creation(aio, needed)

        # Create named fallback feeds only if we cannot find enough usable feeds.
        for feed_name in FEED_NAMES:
            if len(feeds) >= REQUIRED_FEED_COUNT:
                break
            candidate = get_or_create_named_feed(aio, feed_name)
            if all(existing.key != candidate.key for existing in feeds):
                feeds.append(candidate)

    feeds = feeds[:REQUIRED_FEED_COUNT]

    feed_group_ids = {}
    for raw_feed in get_all_feeds_raw(aio):
        key = raw_feed.get("key")
        if not key:
            continue
        group_info = raw_feed.get("group") or {}
        feed_group_ids[key] = group_info.get("id")

    for index, feed in enumerate(feeds):
        total = ensure_min_data(
            aio,
            feed.key,
            MIN_DATAPOINTS_PER_FEED,
            include_location=(index == 1),
        )
        print("Feed '{0}' now has at least {1} datapoints (checked total: {2}).".format(
            feed.key,
            MIN_DATAPOINTS_PER_FEED,
            total,
        ))

    if feeds_only:
        print("Feed bootstrap complete. Set FEEDS_ONLY_MODE = False to create dashboards and blocks.")
        return

    dashboard = get_or_create_example_dashboard(aio)

    dashboard_link_targets = [{
        "name": PUBLIC_DASHBOARD_NAME,
        "key": PUBLIC_DASHBOARD_KEY,
        "username": PUBLIC_DASHBOARD_USERNAME,
    }]

    created_blocks = []
    unbound_blocks = []
    for visual_type in BLOCK_TYPES:
        target_feed = get_target_feed_for_block(visual_type, feeds[0], feeds[1])
        target_group_id = None
        if target_feed is not None:
            target_group_id = feed_group_ids.get(target_feed.key)

        # Dashboard block wiring uses feed IDs and layout uses block IDs.
        block = make_block(
            visual_type,
            feeds[0].id,
            feeds[1].id,
            dashboard_link_targets,
            primary_group_id=feed_group_ids.get(feeds[0].key),
            secondary_group_id=feed_group_ids.get(feeds[1].key),
        )
        created = create_block_via_http(aio, dashboard.key, block)

        # Some visual types are accepted by the API but returned without a feed
        # binding. Try a direct block update fallback when that happens.
        if target_feed is not None and not created.block_feeds:
            rebound = try_patch_block_feed_binding(
                aio,
                dashboard.key,
                created.id,
                target_feed,
                group_id=target_group_id,
            )
            if rebound:
                created = Block.from_dict(rebound)

            if not created.block_feeds:
                print(
                    "Warning: block '{0}' ({1}) has no associated feed after creation. "
                    "Attach feed '{2}' manually if needed.".format(
                        created.name,
                        visual_type,
                        target_feed.key,
                    )
                )
                unbound_blocks.append("{0} (target feed: {1})".format(
                    visual_type,
                    target_feed.key,
                ))

        created_blocks.append(created)

    if unbound_blocks:
        raise RuntimeError(
            "Feed association required for all widgets except divider, but these blocks "
            "were created without linked feeds: {0}".format(
                ", ".join(unbound_blocks)
            )
        )

    layout = Layout(
        xl=build_layout(created_blocks, 4),
        lg=build_layout(created_blocks, 4),
        md=build_layout(created_blocks, 2),
        sm=build_layout(created_blocks, 1),
        xs=build_layout(created_blocks, 1),
    )
    aio.update_layout(dashboard.key, layout)

    print("Dashboard created at: https://io.adafruit.com/{0}/dashboards/{1}".format(
        ADAFRUIT_IO_USERNAME,
        dashboard.key,
    ))
    print("Created {0} blocks ({1}).".format(len(created_blocks), ", ".join(BLOCK_TYPES)))


if __name__ == "__main__":
    if not ADAFRUIT_IO_USERNAME or not ADAFRUIT_IO_KEY:
        raise RuntimeError(
            "Missing Adafruit IO credentials. Activate the venv or set "
            "ADAFRUIT_IO_USERNAME and ADAFRUIT_IO_KEY."
        )

    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    main(aio, feeds_only=FEEDS_ONLY_MODE)
