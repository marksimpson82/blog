Personal blog built with Jekyll and Minimal Mistakes.

## Setup
```bash
bundle install
```

```bash
bundle exec jekyll serve
```

## Cheat sheet
### Include image via markdown (will find dead links), no thumbnail
```md
![alt text]({{ '/assets/images/YYYY/MM/some_image.png' | relative_url }})
```

### Generate thumbnails if needed, then include:
Place below contents in `_includes/image.html`
```md
<a href="{{ include.path | relative_url }}">
  <img src="{{ include.thumb | relative_url }}" alt="{{ include.alt }}">
</a>
```

Then include the thumb via:
```md
{% include image.html path="assets/images/full.png" thumb="assets/images/thumb.png" alt="Wile E. Coyote" %}
```
