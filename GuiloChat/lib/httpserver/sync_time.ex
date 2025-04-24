defmodule Httpserver.SyncTime do
  use Plug.Router

  plug :match
  plug :dispatch

  get "/" do
    send_resp(conn, 200, "Bendo")
  end

  get"/:name" do
    send_resp(conn, 200, "Vendo #{name}")
  end


  match _ do
    send_resp(conn, 404, "Ta erro")
  end
end
