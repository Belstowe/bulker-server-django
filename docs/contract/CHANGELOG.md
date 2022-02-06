# Bulker Contract: changelog

## 1.0.3 (06.02.2022)
* Added new service `GET /AllVoted` for flag, did all players vote;
* `DELETE /Votes`: Added possible response `400 Bad Response`.

## 1.0.2 (06.02.2022)
<ul>
<li>Added new service <code>GET /Players/{id}/Vote</code> (gives out the player, whom Player <code>{id}</code> voted for, if one exists);</li>
<li>Moved service <code>DELETE /Players/{subjectid}/Vote/{objectid}</code> to <code>DELETE /Players/{id}/Vote</code> (<code>{objectid}</code> is not required for this action);</li>
<li><code>Player</code> component:
    <ul>
    <li>Some name changes for the sake of standard: <code>isAlive</code> > <code>is_alive</code>, <code>isFertile</code> > <code>fertile</code>, <code>voteSpree</code> > <code>votespree</code>, <code>votedFor</code> > <code>voted_for</code>;</li>
    <li>No longer gives out <code>votespree</code> and <code>voted_for</code> traits;</li>
    </ul>
<li>Successful response status of <code>POST /Players</code> is now <code>201 CREATED</code> (instead of <code>200 OK</code>).</li>
</li>

</ul>

## 1.0.1 (05.02.2022)
* Initial version.