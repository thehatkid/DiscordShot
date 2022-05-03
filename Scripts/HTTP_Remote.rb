#==============================================================================
# ** HTTP_Server
#------------------------------------------------------------------------------
#  This script runs TCP HTTP server inside OneShot.
#==============================================================================

require 'socket'
require 'json'

# Change IP-address and port if you want or leave it
$http_addr = "127.0.0.1"
$http_port = 8481

def log_write(message)
  Dir.mkdir("./Logs") unless File.exists?("./Logs")

  timestamp_file = Time.now.strftime("%Y-%m-%d")
  timestamp_log = Time.now.strftime("%Y-%m-%d %H:%M:%S,%L")

  File.open("./Logs/#{timestamp_file}.log", "a+") do |logfile|
    logfile.write("[#{timestamp_log}] #{message}\n")
  end
end

# Creating TCP HTTP-server with IP and Port destination
tcp_server = TCPServer.new($http_addr, $http_port)

server_thread = Thread.start do
  start_time = Time.now.strftime("%Y-%m-%d %H:%M:%S")
  log_write "HTTP server started in #{start_time} at http://#{$http_addr}:#{$http_port}/"

  loop do
    begin
      # Accept client in new thread
      Thread.start tcp_server.accept do |client|
        sock_domain, remote_port, remote_hostname, remote_ip = client.peeraddr

        http_headers = ""
        while (line = client.gets) && (line != "\r\n")
          http_headers += line
        end

        if header_route = http_headers.match(/^(\S+) (\S+) HTTP\/(\d+.\d+)/)
          http_method = header_route[1]
          http_path = header_route[2]
          http_version = header_route[3]
        else
          # Disconnect client due to invalid HTTP data
          log_write "Disconnect #{remote_ip}:#{remote_port} due to invalid HTTP"
          client.close
          next
          log_write "bruh"
        end

        if content_length = http_headers.match(/^Content-Length: (\d+)/i)
          content = client.read(content_length[1].to_i)
        end

        log_write "#{remote_ip}:#{remote_port} - \"#{http_method} #{http_path} HTTP/#{http_version}\""
        routes = http_path.split("/")

        case routes[1]
        when "oneshot"
          if routes.length >= 3
            case routes[2]
            when "lastinputs"
              if http_method == "GET"
                client.write(HTTP.response_data(200, $game_system.ds_last_inputs.to_json, "application/json"))
              elsif http_method == "POST"
                begin
                  json_data = JSON.parse(content)
                rescue
                  client.write(HTTP.response(400, "Invalid JSON"))
                  next
                end
                if json_data.has_key? "author"
                  if json_data.has_key? "input"
                    DiscordShot.last_input_append(json_data["author"], json_data["input"])
                    client.write(HTTP.response(204, ""))
                  else
                    client.write(HTTP.response_data(400, {:ok => false, :error => "No \"input\" key in JSON"}.to_json, "application/json"))
                  end
                else
                  client.write(HTTP.response_data(400, {:ok => false, :error => "No \"author\" key in JSON"}.to_json, "application/json"))
                end
              end
            when "message"
              if http_method == "POST"
                begin
                  json_data = JSON.parse(content)
                rescue
                  client.write(HTTP.response(400, "Invalid JSON"))
                  next
                end
                if json_data.has_key? "author"
                  if json_data.has_key? "text"
                    if json_data.has_key? "face"
                      if !File.exists?("Graphics/Faces/#{json_data["face"]}.png")
                        client.write(HTTP.response_data(404, {:ok => false, :error => "No face \"#{json_data["face"]}\" in game"}.to_json, "application/json"))
                      else
                        if $game_temp.message_window_showing
                          client.write(HTTP.response_data(409, {:ok => false, :error => "Message box is already showing"}.to_json, "application/json"))
                        else
                          $game_temp.message_text = json_data["text"]
                          $game_temp.message_face = json_data["face"]
                          DiscordShot.last_input_append(json_data["author"], "Message")
                          client.write(HTTP.response(204, ""))
                        end
                      end
                    else
                      client.write(HTTP.response_data(400, {:ok => false, :error => "No \"face\" key in JSON"}.to_json, "application/json"))
                    end
                  else
                    client.write(HTTP.response_data(400, {:ok => false, :error => "No \"text\" key in JSON"}.to_json, "application/json"))
                  end
                else
                  client.write(HTTP.response_data(400, {:ok => false, :error => "No \"author\" key in JSON"}.to_json, "application/json"))
                end
              end
            when "faces"
              facelist = Dir["Graphics/Faces/*.*"]
              facelist.each_with_index { |path, index| facelist[index] = File.basename(path, ".*") }
              client.write(HTTP.response(200, facelist.join(", ")))
            else
              client.write(HTTP.response(404, "Unknown method \"#{routes[2]}\""))
            end
          else
            client.write(HTTP.response(400, "No method in \"/#{routes[1]}\" route"))
          end
        else
          client.write(HTTP.response(200, "[Hello, my friend.]"))
        end

        client.close
      rescue Exception => e
        stacktrace = e.inspect + "\n"
        for i in 0..(e.backtrace.length - 1)
          stacktrace += ("> " + e.backtrace[i].to_s + "\n")
        end

        client.write(HTTP.response(500, "Raised exception while processing HTTP request:\n\n#{stacktrace}"))
        client.close
      end
    end
  end
end
