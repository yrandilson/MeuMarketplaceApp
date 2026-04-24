package com.example.meumarketplace.adapters
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.meumarketplace.R
import com.example.meumarketplace.models.Anuncio

class AnuncioAdapter(private val anuncios: MutableList<Anuncio>) : RecyclerView.Adapter<AnuncioAdapter.AnuncioViewHolder>() {
    class AnuncioViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val textTitulo: TextView = itemView.findViewById(R.id.textTitulo)
        val textPreco: TextView = itemView.findViewById(R.id.textPreco)
    }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AnuncioViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_anuncio, parent, false)
        return AnuncioViewHolder(view)
    }
    override fun onBindViewHolder(holder: AnuncioViewHolder, position: Int) {
        val anuncio = anuncios[position]
        holder.textTitulo.text = anuncio.titulo
        holder.textPreco.text = "R$ ${anuncio.preco}"
    }
    override fun getItemCount() = anuncios.size
    fun updateAnuncios(novosAnuncios: List<Anuncio>) {
        anuncios.clear()
        anuncios.addAll(novosAnuncios)
        notifyDataSetChanged()
    }
}