defmodule Httpserver.SyncTime do
  import Plug.Conn

  def init(options), do: options

  def call(conn, _opts) do
    send_resp(put_resp_content_type(conn, "text/plain"), 200, "Página para sincronização do tempo com relógio de berkeley\n")
  end
end
