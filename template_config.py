# Auto-generated template configuration
from typing import Dict

# Template layout configuration
LAYOUT_MAPPING = {
    'title_slide': {
        'index': 0,
        'placeholders': {
            'title_1': {'type': CENTER_TITLE (3), 'idx': 0},
            'subtitle_2': {'type': SUBTITLE (4), 'idx': 1},
            'date_placeholder_3': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_4': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_5': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'title_and_content': {
        'index': 1,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'content_placeholder_2': {'type': OBJECT (7), 'idx': 1},
            'date_placeholder_3': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_4': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_5': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'section_header': {
        'index': 2,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'text_placeholder_2': {'type': BODY (2), 'idx': 1},
            'date_placeholder_3': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_4': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_5': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'two_content': {
        'index': 3,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'content_placeholder_2': {'type': OBJECT (7), 'idx': 1},
            'content_placeholder_3': {'type': OBJECT (7), 'idx': 2},
            'date_placeholder_4': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_5': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_6': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'comparison': {
        'index': 4,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'text_placeholder_2': {'type': BODY (2), 'idx': 1},
            'content_placeholder_3': {'type': OBJECT (7), 'idx': 2},
            'text_placeholder_4': {'type': BODY (2), 'idx': 3},
            'content_placeholder_5': {'type': OBJECT (7), 'idx': 4},
            'date_placeholder_6': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_7': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_8': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'title_only': {
        'index': 5,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'date_placeholder_2': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_3': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_4': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'blank': {
        'index': 6,
        'placeholders': {
            'date_placeholder_1': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_2': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_3': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'content_with_caption': {
        'index': 7,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'content_placeholder_2': {'type': OBJECT (7), 'idx': 1},
            'text_placeholder_3': {'type': BODY (2), 'idx': 2},
            'date_placeholder_4': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_5': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_6': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'picture_with_caption': {
        'index': 8,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'picture_placeholder_2': {'type': PICTURE (18), 'idx': 1},
            'text_placeholder_3': {'type': BODY (2), 'idx': 2},
            'date_placeholder_4': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_5': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_6': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'title_and_vertical_text': {
        'index': 9,
        'placeholders': {
            'title_1': {'type': TITLE (1), 'idx': 0},
            'vertical_text_placeholder_2': {'type': BODY (2), 'idx': 1},
            'date_placeholder_3': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_4': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_5': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
    'vertical_title_and_text': {
        'index': 10,
        'placeholders': {
            'vertical_title_1': {'type': TITLE (1), 'idx': 0},
            'vertical_text_placeholder_2': {'type': BODY (2), 'idx': 1},
            'date_placeholder_3': {'type': DATE (16), 'idx': 10},
            'footer_placeholder_4': {'type': FOOTER (15), 'idx': 11},
            'slide_number_placeholder_5': {'type': SLIDE_NUMBER (13), 'idx': 12},
        }
    },
}

# Slide type to layout mapping
SLIDE_TYPE_LAYOUTS = {
    'title': 'title_slide',
    'content': 'content',
    'section': 'section',
    'two_content': 'two_content',
    'summary': 'content',
    'quiz': 'content',
    'lab': 'content'
}

def get_layout_info(layout_type: str) -> Dict:
    """Get layout information for a specific type"""
    layout_name = SLIDE_TYPE_LAYOUTS.get(layout_type)
    return LAYOUT_MAPPING.get(layout_name) if layout_name else None

def get_placeholder_info(layout_type: str, placeholder_name: str) -> Dict:
    """Get placeholder information for a specific layout and placeholder"""
    layout_info = get_layout_info(layout_type)
    if layout_info:
        return layout_info['placeholders'].get(placeholder_name)
    return None
