#==============================================================================
# ** DiscordShot
#------------------------------------------------------------------------------
#  This is DiscordShot mod script.
#==============================================================================

module DiscordShot

  def self.last_input_append(last_author, last_input)
    if $game_system.ds_last_inputs['authors'].size >= 5
      # droping last author
      $game_system.ds_last_inputs['authors'] = $game_system.ds_last_inputs['authors'].drop(1)
      # appending first author
      $game_system.ds_last_inputs['authors'] << last_author
    else
      # appending first author
      $game_system.ds_last_inputs['authors'] << last_author
    end

    if $game_system.ds_last_inputs['inputs'].size >= 5
      # droping last input
      $game_system.ds_last_inputs['inputs'] = $game_system.ds_last_inputs['inputs'].drop(1)
      # appending first input
      $game_system.ds_last_inputs['inputs'] << last_input
    else
      # appending first author
      $game_system.ds_last_inputs['inputs'] << last_input
    end
  end

end
