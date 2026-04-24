package com.example.meumarketplace.adapters
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.meumarketplace.R
import com.example.meumarketplace.models.Mensagem
import com.google.firebase.auth.FirebaseAuth

class MensagemAdapter(private val mensagens: List<Mensagem>) : RecyclerView.Adapter<MensagemAdapter.MensagemViewHolder>() {
    class MensagemViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val textMensagem: TextView = itemView.findViewById(R.id.textMensagem)
    }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MensagemViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_mensagem, parent, false)
        return MensagemViewHolder(view)
    }
    override fun onBindViewHolder(holder: MensagemViewHolder, position: Int) {
        val mensagem = mensagens[position]
        holder.textMensagem.text = mensagem.texto
        if (mensagem.deUsuarioId == FirebaseAuth.getInstance().currentUser?.uid) {
            holder.textMensagem.setBackgroundResource(R.drawable.bubble_sent)
        } else {
            holder.textMensagem.setBackgroundResource(R.drawable.bubble_received)
        }
    }
    override fun getItemCount() = mensagens.size
}