# Custom Printed Book

I printed 1 copy of the "Game Boy Programming Manual v1.1" for myself.
I do not like to read so much information on a screen and love books, so here are sources of the printed book.

I just created a cover and first page, appended to the [manual itself](../specs/gameboy-programming-v1.1.pdf).

Fonts:

- [Early GameBoy](https://www.dafont.com/early-gameboy.font), by Jimmy Campbell.
- [Fira Code](https://www.fontsquirrel.com/fonts/fira-code), by Mozilla.
- [Fira Sans](https://www.fontsquirrel.com/fonts/fira-sans), by Mozilla.

The Ninento Game Boy logo is from [Wikipedia](https://en.wikipedia.org/wiki/File:Gameboy_logo.svg).

## Commands

Some useful command used to generate the book:

```bash
# Merge the first page to the manual
$ pdftk \
    "first-page.pdf" \
    "../specs/gameboy-programming-v1.1.pdf" \
    cat output \
    "book-unoptimized.pdf"

# Optimize the final PDF
$ gs \
    -o "book.pdf" \
    -sDEVICE=pdfwrite \
    -dPDFSETTINGS=/prepress \
    -dEmbedAllFonts=true \
    "book-unoptimized.pdf"
```

[FR] Plus de détails [ici](http://www.tiger-222.fr/?d=2019/12/07/14/59/33-manipulation-de-fichiers-pdf).
