# Bulker Contract: changelog

## 1.0.3 (06.02.2022)
* Added new service `GET /AllVoted` for flag, did all players vote?

## 1.0.2 (06.02.2022)
<ul>
<li>Added new service `GET /Players/{id}/Vote` (gives out the player, whom Player `{id}` voted for, if one exists);</li>
<li>Moved service `DELETE /Players/{subjectid}/Vote/{objectid}` to `DELETE /Players/{id}/Vote` (`{objectid}` is not required for this action);</li>
<li>`Player` component:
    <ul>
    <li>Some name changes for the sake of standard: `isAlive` > `is_alive`, `isFertile` > `fertile`, `voteSpree` > `votespree`, `votedFor` > `voted_for`;</li>
    <li>No longer gives out `votespree` and `voted_for` traits;</li>
    </ul>
<li>Successful response status of `POST /Players` is now `201 CREATED` (instead of `200 OK`).</li>
</li>

</ul>

## 1.0.1 (05.02.2022)
* Initial version.