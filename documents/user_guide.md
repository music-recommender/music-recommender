# User guide

- Find the app online.
    - Navigate to the [app](https://music-recommender.github.io/music-recommender/app/app.html).
    - Loading the website might take around half a minute because <em>PyScript</em> based application is being prepared and its packages are downloaded.  

- Selecting a song
    - Move your cursor on top of the visible <em>Songs</em>-table.
    - If the cursor is on top of a row (some song), the hovering tool should highlight that row.
    - Select a song by clicking the highlighted row.
    - The selected song should appear on the <em>Selected</em>-table below the <em>Songs</em>-table.

- Selecting multiple songs
    - Selecting multiple songs happens same way as selecting one song (more above).
    - Note selecting a song more than once is not possible.

- See recommendations
    - After a song is selected and the <em>Selected</em>-table is updated, recommendations are automatically calculated based on the selected songs. A new table called <em>Recommendations</em> appears at the bottom which has five recommended songs.

- Sorting and filtering songs
    - Sorting songs based on a column's values can be done by clicking on the column's header. On the right side of each header there exists an arrow which corresponds to either descending or ascending ordering.
    - There exists a filter for each column applied on the <em>Songs</em>-table.
        - Title:
            - Filtering is based on a string pattern input.
            - Case-insensitive
            - E.g. "Never Gonna Give You Up", "never gonna give"
        - Artist
            - Filtering is based on a string pattern input.
            - Case-insensitive
            - E.g. "bob", "Bob Hope"
        - Location
            - Filtering is based on a string pattern input.
            - Case-insensitive
            - E.g. "Germany", "finland"
        - Genres
            - Filtering is based on string pattern inputs separated with a space character (" ").
            - Case-insensitive
            - E.g. "rock", "rock heavy death metal"
        - Tempo
            - Include only those songs that have values inside the slider's interval.
            - The slider's start and end values correspond to the minimum and maximum values of the Tempo-column.
        - Year
            - Include only songs with year inside the slider's interval.
            - The slider's start and end values correspond to the minimum and maximum values of the Year-column.

- Changing pages
    - On the <em>Songs</em>-table footer (below visible songs), there is a paginator which allows you to change pages.

- Remove a song from selected songs
    - Removing a song from the <em>Selected</em>-table works also by clicking on a highlighted row (as when selecting a song).
    - Removed song disappears from the <em>Selected</em>-table. It is selectable on the <em>Songs</em>-table again.

