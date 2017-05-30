#! /usr/bin/env python3
# coding=utf-8

import base64
import svgwrite


def export_as_svg(profile, path, sheet):
    """Export the character's profile to a formatted SVG file.

    Args:
        profile: an instance of scox.character.Character.
        path: path to a folder where to write the resulting SVG file.
        sheet: a PNG file representing the (empty) character sheet to be
        exported.
    """
    with open(sheet, 'rb') as image_file:
        encoded_str = 'data:image/png;base64,' + \
                      base64.b64encode(image_file.read()).decode()
    fnt_skl = "font-size:40pt;font-family:'Traveling _Typewriter'"
    dwg = svgwrite.Drawing(path, size=(2479, 3504))
    # background
    dwg.add(dwg.image(encoded_str, size=(2479, 3504)))
    # identity info
    dwg.add(dwg.text(profile.get_name(),
                     x=[profile.get_name_coords()[0]],
                     y=[profile.get_name_coords()[1]],
                     style=fnt_skl))
    dwg.add(dwg.text(str(profile.get_level()),
                     x=[profile.get_lvl_coords()[0]],
                     y=[profile.get_lvl_coords()[1]],
                     style=fnt_skl))
    dwg.add(dwg.text(profile.get_superior(),
                     x=[profile.get_sup_coords()[0]],
                     y=[profile.get_sup_coords()[1]],
                     style=fnt_skl))
    # attributes
    export_attributes_as_svg(profile, dwg)
    # side values
    export_values_as_svg(profile, dwg)
    # skills
    export_skills_as_svg(profile, dwg)
    export_exotic_skills_as_svg(profile, dwg)
    # powers
    export_powers_as_svg(profile, dwg)
    dwg.save()


def export_attributes_as_svg(profile, drawing):
    """Write the character's attributes on an SVG drawing.

    Args:
        profile: an instance of scox.character.Character.
        drawing: a writable SVG drawing.
    """
    fnt = "font-size:100pt;font-family:'Baron Kuffner'"
    for a in profile.get_attributes().values():
        drawing.add(drawing.text(a.get_cli_rank(), x=[a.get_x()],
                                 y=[a.get_y()], style=fnt))


def export_skills_as_svg(profile, drawing):
    """Write the character's skills on an SVG drawing.

    Args:
        profile: an instance of scox.character.Character.
        drawing: a writable SVG drawing.
    """
    fnt = "font-size:40pt;font-family:'Traveling _Typewriter'"
    fnt_sml = "font-size:32pt;font-family:'Traveling _Typewriter'"
    sp_shift = -549
    m_shift = -527
    p_and_s = {}
    p_and_s.update(profile.get_primary_skills())
    p_and_s.update(profile.get_secondary_skills())
    for s in p_and_s.values():
        if s.is_usable():
            if s.is_invariant():  # only one possibility : Langues
                v_list = ''
                for v in s.get_varieties():
                    v_list += v + ', '
                drawing.add(drawing.text(v_list.rstrip(', '),
                                         x=[s.get_x()], y=[s.get_y()],
                                         style=fnt_sml))
            else:
                drawing.add(drawing.text(s.get_cli_rank(), x=[s.get_x()],
                                         y=[s.get_y()], style=fnt))
                if s.is_specific():
                    sp = s.get_specialization()
                    drawing.add(
                        drawing.text(sp.get_cli_rank(), x=[sp.get_x()],
                                     y=[sp.get_y()], style=fnt))
                    drawing.add(
                        drawing.text(sp.get_name(),
                                     x=[sp.get_x() + sp_shift],
                                     y=[sp.get_y()], style=fnt_sml))
                elif s.is_multiple():
                    s_list = ''
                    for v in s.get_varieties():
                        s_list += v + ', '
                    drawing.add(drawing.text(s_list.rstrip(', '),
                                             x=[s.get_x() + m_shift],
                                             y=[s.get_y()], style=fnt_sml))


def export_exotic_skills_as_svg(profile, drawing):
    """Write the character's exotic skills on an SVG drawing.

    Args:
        profile: an instance of scox.character.Character.
        drawing: a writable SVG drawing.
    """
    fnt = "font-size:40pt;font-family:'Traveling _Typewriter'"
    fnt_sml = "font-size:36pt;font-family:'Traveling _Typewriter'"
    v_shift = 62.5
    e_shift = -807
    ch_shift = 125
    it = 0
    for e in profile.get_exotic_skills().values():
        if e.is_usable():
            drawing.add(drawing.text(e.get_cli_rank(), x=[e.get_x()],
                                     y=[e.get_y() + it * v_shift],
                                     style=fnt))
            drawing.add(drawing.text(e.get_name(),
                                     x=[e.get_x() + e_shift],
                                     y=[e.get_y() + it * v_shift],
                                     style=fnt_sml))
            if e.get_governing_attribute() is not None:
                drawing.add(drawing.text(
                    e.get_governing_attribute().get_name()[:3],
                    x=[e.get_x() + ch_shift],
                    y=[e.get_y() + it * v_shift], style=fnt_sml))
            it += 1


def export_powers_as_svg(profile, drawing):
    """Write the character's side values on an SVG drawing.

    Args:
        profile: an instance of scox.character.Character.
        drawing: a writable SVG drawing.
    """
    fnt = "font-size:36pt;font-family:'Traveling _Typewriter'"
    fnt_big = "font-size:40pt;font-family:'Traveling _Typewriter'"
    fnt_sml = "font-size:28pt;font-family:'Traveling _Typewriter'"
    n_shift = -835
    c_shift = 125
    for pw in profile.get_powers().values():
        if not pw.is_invariant():
            drawing.add(drawing.text(pw.get_cli_rank(), x=[pw.get_x()],
                                     y=[pw.get_y()], style=fnt_big))
        drawing.add(drawing.text(pw.get_name(), x=[pw.get_x() + n_shift],
                                 y=[pw.get_y()], style=fnt))
        drawing.add(drawing.text(pw.get_cost(), x=[pw.get_x() + c_shift],
                                 y=[pw.get_y()], style=fnt_sml))


def export_values_as_svg(profile, drawing):
    """Write the character's side values on an SVG drawing.

    Args:
        profile: an instance of scox.character.Character.
        drawing: a writable SVG drawing.
    """
    size = '40pt' if profile.get_nature() == 'Demon' else '36pt'
    fnt = "font-size:" + size + ";font-family:'Traveling _Typewriter'"
    for v in profile.get_side_values().values():
        drawing.add(drawing.text(v.get_cli_rank(), x=[v.get_x()],
                                 y=[v.get_y()], style=fnt))
