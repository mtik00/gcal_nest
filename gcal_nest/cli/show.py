#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#  Copyright (C) 2017 Broadcom Ltd.  All rights reserved.                     #
#                                                                             #
###############################################################################
'''
This module holds the cli `show` commands
'''

# Imports #####################################################################
import click

from ..gcal import get_next_events
from ..nest import get_napi_thermostat
from ..helpers import print_log

# Metadata ####################################################################
__author__ = 'Timothy McFadden'
__creationDate__ = '11-JUN-2017'
__license__ = 'Proprietary'


# Globals #####################################################################
@click.group()
def show():
    '''Show information'''
    ctx = click.get_current_context()

    # No reason to continue if we're in quiet mode
    if ctx.obj.quiet:
        ctx.exit()


@show.command()
@click.option(
    '--max-events', default=10, help='maximum number of events to show')
def events(max_events):
    '''Display the next events from Google calendar'''
    ctx = click.get_current_context().obj

    q = 'nest'
    if ctx.debug:
        q = 'nestd'

    nest_events = get_next_events(max_results=max_events, q_filter=q)

    for event in nest_events:
        print_log(
            "{:<19s}({:^9}) {}".format(
                event.scheduled_date.format('YYYY-MM-DD h:mmA'),
                event.state,
                event.name)
        )


@show.command()
def cache():
    '''
    Shows the cached events
    '''
    ctx = click.get_current_context().obj

    # For the pager to work, we need to create one big string.
    str_events = []
    for event in ctx.cache.events():
        str_events.append(
            "{:<19s}({:^9}) {}".format(
                event.scheduled_date.format('YYYY-MM-DD h:mmA'),
                event.state,
                event.name)
        )

    click.echo_via_pager("\n".join(str_events))


@show.command()
def thermostat():
    '''Show the current thermostat info'''

    ctx = click.get_current_context().obj
    thermostat = get_napi_thermostat(ctx)

    print_log(
        '%s : %s' % (
            thermostat.structure.name,
            thermostat.name)
    )

    setpoint = "%s%s (%s)" % (thermostat.target, thermostat.temperature_scale, thermostat.mode)
    if thermostat.mode.lower() == 'eco':
        setpoint = "%s%s (eco)" % (thermostat.eco_temperature.low, thermostat.temperature_scale)
    print_log('...current setpoint: %s' % setpoint)

    print_log(
        '...current temperature: %s%s' % (
            thermostat.temperature,
            thermostat.temperature_scale
        )
    )

    print_log(
        '...current humidity: %s%%' % thermostat.humidity
    )

    print_log(
        '...state: %s' % thermostat.hvac_state
    )

    print_log(
        '...eco temperatures: low={low}{scale}, high={high}{scale}'.format(
            low=thermostat.eco_temperature.low,
            scale=thermostat.temperature_scale,
            high=thermostat.eco_temperature.high
        )
    )