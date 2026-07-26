# MASDS WCAG 2.1 AA alternative

This directory is a separate, best-effort accessible version of the MASDS mockup. The original `masds-mockup` directory has not been modified as part of this accessibility pass.

## Improvements included

- A keyboard-visible “Skip to main content” link on every page.
- Consistent, high-contrast keyboard focus indicators.
- Underlined in-content text links and distinct button treatments.
- Responsive navigation and content reflow, including wrapped top-bar and navigation text.
- Reduced-motion support for visitors who request it in their operating system.
- One descriptive `h1`, consistent heading order, and labeled content sections on every page.
- Ordered-list semantics for application and thesis steps.
- Descriptive alternative text for meaningful images and empty alternative text for decorative or text-redundant logos.
- Accessible names that announce partner links opening in a new tab.
- A descriptive title and accessible-format guidance for the embedded program video.
- Captions, column headers, and row headers for all data tables.
- Keyboard-focusable, labeled table regions so wide tables can be scrolled without a pointer.
- Existing FAQ questions retained as native `details` and `summary` controls with stronger focus styling.
- Layout motion disabled when `prefers-reduced-motion: reduce` is active.

## Checks completed

The included `accessibility-audit.py` checks all nine HTML pages for:

- document language, titles, viewport metadata, and page landmarks;
- skip links, unique IDs, and heading order;
- accessible names for links, images, and iframes;
- natural keyboard focus order;
- labeled sections and valid FAQ disclosure structure;
- table captions, scoped headers, and labeled scroll regions; and
- broken local links and media references.

The source-level audit completed with no findings. Key foreground/background color combinations were also calculated against WCAG contrast thresholds. The lowest normal-text combination checked was `#677487` on white at approximately 4.75:1, above the 4.5:1 AA requirement.

To rerun the audit from this directory:

```powershell
python .\accessibility-audit.py
```

## Manual verification still required

Automated and source-level checks cannot establish full WCAG conformance. Before publishing, complete:

- a full keyboard-only review in current desktop and mobile browsers;
- testing at 200% text size and 400% browser zoom;
- screen-reader testing with NVDA or JAWS on Windows and VoiceOver on Apple devices;
- verification that the YouTube video has accurate synchronized captions, an accurate transcript, and audio description or an equivalent alternative when visual information is not conveyed in the audio;
- review of reading order and announcements in each supported browser/screen-reader combination; and
- ongoing accessibility review whenever content, links, images, or components change.

Third-party destinations, including UCLA systems, YouTube, and partner websites, are outside the conformance scope of these local files.
