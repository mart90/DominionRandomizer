// https://docs.google.com/spreadsheets/d/1yfrDG-oX6dJjmni3HjUrp5zEyQHHli4SWqlpEUixHNU/edit#gid=0

function makeDict() {
    s = SpreadsheetApp.getActiveSheet()

    var date = s.getRange(33, 2).getValue()
    var withcolonies = s.getRange(34, 2).getValue()
    var withplatinum = s.getRange(35, 2).getValue()
    
    var players = []
    var playernames = s.getRange(2, 2, 1, 6).getValues()[0]
    for (var i = 0; i < playernames.length; i++) {
        if (playernames[i] == "") {
            continue
        }

        var playercolumn = i + 2
        players.push({
            'name': playernames[i],
            'column': playercolumn,
            'bid': s.getRange(3, playercolumn).getValue(),
            'score': s.getRange(4, playercolumn).getValue(),
            'turn': s.getRange(5, playercolumn).getValue()
        })
    }

    var cards = []
    var cardnames = s.getRange(8, 1, 10).getValues()
    for (var i = 0; i < cardnames.length; i++) {
        var cardrow = i + 8
        cards.push({
            'name': cardnames[i],
            'buys': []
        })

        card = cards[cards.length - 1]
        for (var a = 0; a < players.length; a++) {
            playerbuys = s.getRange(cardrow, players[a]['column']).getValue()
            if (playerbuys) {
                card['buys'].push({
                    'player': players[a]['name'],
                    'buys': playerbuys
                })
            }
        }
    }

    var votedcards = []
    var votedcardnames = s.getRange(19, 1, 12).getValues()
    for (var i = 0; i < votedcardnames.length; i++) {
        if (votedcardnames[i] == "") {
            continue
        }

        var votedcardrow = i + 19
        votedcards.push({
            'name': votedcardnames[i],
            'votes': [],
            'initiator': ""
        })

        votedcard = votedcards[votedcards.length - 1]
        for (var a = 0; a < players.length; a++) {
            var vote = s.getRange(votedcardrow, players[a]['column']).getValue()
            votedcard['votes'].push({
                'player': players[a]['name'],
                'vote': vote
            })

            if (vote == 2) {
                votedcard['initiator'] = players[a]['name']
            }
        }
    }

    var pydict = 
        '{ "date": "' + date +
        '", "with colonies": ' + withcolonies +
        ', "with platinum": ' + withplatinum +
        ', "players": [ '

    for (var i = 0; i < players.length; i++) {
        p = players[i]
        pydict += 
            '{ "name": "' + p['name'] + 
            '", "bid": ' + p['bid'] +
            ', "score": ' + p['score'] + 
            ', "turn": ' + p['turn'] + ' }, '
    }

    pydict += '], "cards": [ '
    for (var i = 0; i < cards.length; i++) {
        c = cards[i]
        pydict += 
            '{ "name": "' + c['name'] +
            '", "buys": [ '
        
        for (var a = 0; a < c.buys.length; a++) {
            b = c.buys[a]
            pydict += 
                '{ "player": "' + b['player'] +
                '", "amount bought": ' + b['buys'] + ' }, '
        }

        pydict += ']}, '
    }

    pydict += '], "votes": [ '
    for (var i = 0; i < votedcards.length; i++) {
        vc = votedcards[i]
        pydict += 
            '{ "card": "' + vc['name'] +
            '", "initiator": "' + vc['initiator'] +
            '", "votes": [ '

        for (var a = 0; a < vc.votes.length; a++) {
            v = vc.votes[a]
            var vote = (v['vote'] == 2) ? 1 : v['vote']
            pydict += 
                '{ "player": "' + v['player'] +
                '", "vote": ' + vote + ' }, '
        }

        pydict += ']}, '
    }

    pydict += ']}'

    for (var i = 3; i < 1000; i++) {
        var r = s.getRange(i, 10)
        if (r.getValue() == "") {
            r.setValue(pydict)
            break
        }
    }
}

function makeArray() {
    var s = SpreadsheetApp.getActiveSheet()
    
    var arr = 'games = [' 
    
    var dicts = s.getRange(3, 10, 1000).getValues()
    for (var i = 0; i < dicts.length; i++) {
        var dict = dicts[i]
        if (dict == "") {
            break
        }
        
        arr += dict + ','
    }
    
    arr += ']'
    s.getRange(2, 11).setValue(arr)
}
