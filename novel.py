"""
Generate a novel out of nothing.
"""
import random


def get_stage(word_count, stage_length):
    """Get the stage out of the current word count and the average stage length."""
    return int(word_count / stage_length) + 1


def create_first_half_section(sections, stage, max_words):
    """Generate a section for the first half of the novel."""
    number = len(sections) + 1
    if stage == 1:
        intro = "Orphan-YOU: Introduction to the Status Quo."
        loc_name = 'Normloc#%i' % number
    elif stage == 2:
        intro = "Orphan-NEED: Introduction of the Want."
        loc_name = 'Normloc#%i' % number
    elif stage == 3:
        intro = "Reaction-Wanderer-GO: Enter the new world."
        loc_name = 'Xraloc#%i' % number
    elif stage == 4:
        intro = "Reaction-Wanderer-SEARCH: Adapt to the new world."
        loc_name = 'Xraloc#%i' % number
    text = intro + " I tried my luck at the next location, {}.\
    And there I used tool#{} for at most {} words.".format(
        loc_name, number, max_words)
    rand = random.randint(0, 10)
    if rand < 2:
        text += " It worked out pretty well."
    elif rand < 5:
        text += " Unfortunately, I lost a lot of money that way."
    effects = ['effect#%i-%i' % (number, x)
               for x in xrange(random.randint(1, 3))]
    if sections:
        random.shuffle(sections[-1]['effects'])

        used = [sections[-1]['effects'][0]]
        if sections[-1]['rest'] and random.randint(0, 1):
            random.shuffle(sections[-1]['rest'])
            used.append(sections[-1]['rest'][0])
            rest = sections[-1]['effects'][1:] + sections[-1]['rest'][1:]
        else:
            rest = sections[-1]['effects'][1:] + sections[-1]['rest']
        text += " {} had an effect on this.".format(
            " and ".join(used))
    else:
        rest = []
    return {
        'count': len(text.split()),
        'stage': stage,
        'section': number,
        'text': text,
        'location': 'loc#{}'.format(number),
        'tool': 'tool#{}'.format(number),
        'effects': effects,
        'rest': rest
    }


def create_second_half_section(first_half_sections, second_half_sections, loc, tool):
    """Generate a Section for the second half of the novel."""
    stage = 9 - first_half_sections[loc]['stage']
    number = len(first_half_sections) + len(second_half_sections) + 1
    count = first_half_sections[loc]['count']
    if stage == 5:
        intro = "Proaction-Warrior-FIND: Find what you wanted."
    elif stage == 6:
        intro = "Proaction-Warrior-TAKE: Pay the price."
    elif stage == 7:
        intro = "Martyr-RETURN: Return to old world."
    elif stage == 8:
        intro = "Martyr-CHANGE: Change."
    text = intro + (" Now, I stayed in " if tool == 0 else "I went back to ")
    text += "{} where I used {} for {} words.".format(
        first_half_sections[loc]['location'], first_half_sections[tool]['tool'], count)
    effects = ['effect#%i-%i' % (number, x)
               for x in xrange(random.randint(1, 3))]
    if second_half_sections:
        sections = second_half_sections
    else:
        sections = first_half_sections
    random.shuffle(sections[-1]['effects'])
    used = [sections[-1]['effects'][0]]
    if sections[-1]['rest'] and random.randint(0, 1):
        random.shuffle(sections[-1]['rest'])
        used.append(sections[-1]['rest'][0])
        rest = sections[-1]['effects'][1:] + sections[-1]['rest'][1:]
    else:
        rest = sections[-1]['effects'][1:] + sections[-1]['rest']
    text += " {} had an effect on this.".format(
        " and ".join(used))
    while (len(text.split()) < count):
        text += " Bla bla bla."
    return {
        'count': len(text.split()),
        'stage': stage,
        'section': number,
        'text': text,
        'effects': effects,
        'rest': rest
    }


def create_location():
    """Generates a random location."""
    number = random.randint(1, 2500)
    return number


def create_tool():
    """Generates a random tool."""
    pass


def create_novel(filepath, min_words=50000):
    """Generate a novel with at least min_words wordst"""
    word_count = 0
    half_count = round(min_words / 2.)
    stage_length = round(min_words / 8.)

    # set up
    # tool_set = ['tool #%i' % (i + 1) for i in xrange(2500)]
    # location_set = ['location #%i' % (i + 1) for i in xrange(2500)]

    # Create First Half
    first_half_sections = []
    print "stage_length", stage_length
    while word_count < half_count:
        stage = get_stage(word_count, stage_length)
        print word_count, stage
        first_half_sections.append(
            create_first_half_section(first_half_sections, stage,
                                      stage * stage_length - word_count))
        word_count += first_half_sections[-1]['count']
    print word_count, 1 + (1. * word_count) // stage_length, len(first_half_sections)
    first_half = len(first_half_sections)

    # Create Second Half
    second_half_sections = []
    for i in xrange(first_half):
        print word_count
        second_half_sections.append(create_second_half_section(
            first_half_sections, second_half_sections, first_half - 1 - i, i))
        word_count += second_half_sections[-1]['count']
    print word_count

    # Save Novel
    with open(filepath, 'w+') as novel_file:
        current_stage = 1
        novel_file.write('# Novel\n\n## Stage #1\n')
        cc = 0
        for section in first_half_sections + second_half_sections:
            if section['stage'] > current_stage:
                current_stage = section['stage']
                novel_file.write('\n## Stage #%i\n' % section['stage'])
            novel_file.write(('\n### Section #%i\n\n' %
                              section['section']) + section['text'] + '\n')
            cc += section['count']
    print "WORDS:",cc

if __name__ == '__main__':
    create_novel('test.md', min_words=50000)
