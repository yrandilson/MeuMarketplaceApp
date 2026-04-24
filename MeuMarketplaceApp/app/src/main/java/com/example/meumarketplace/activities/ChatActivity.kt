package com.example.meumarketplace.activities
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.meumarketplace.adapters.MensagemAdapter
import com.example.meumarketplace.models.Mensagem
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import kotlinx.android.synthetic.main.activity_chat.*

class ChatActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    private lateinit var mensagemAdapter: MensagemAdapter
    private val mensagens = mutableListOf<Mensagem>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        val outroUsuarioId = intent.getStringExtra("outroUsuarioId") ?: return
        mensagemAdapter = MensagemAdapter(mensagens)
        recyclerViewMensagens.layoutManager = LinearLayoutManager(this)
        recyclerViewMensagens.adapter = mensagemAdapter
        db.collection("mensagens")
            .whereIn("dePara", listOf(
                "${auth.currentUser?.uid}_$outroUsuarioId",
                "$outroUsuarioId_${auth.currentUser?.uid}"
            ))
            .orderBy("data", Query.Direction.ASCENDING)
            .addSnapshotListener { snapshot, _ ->
                mensagens.clear()
                snapshot?.documents?.forEach { doc ->
                    doc.toObject(Mensagem::class.java)?.let { mensagens.add(it) }
                }
                mensagemAdapter.notifyDataSetChanged()
                recyclerViewMensagens.scrollToPosition(mensagens.size - 1)
            }
        btnEnviar.setOnClickListener {
            val texto = editTextMensagem.text.toString().trim()
            if (texto.isNotEmpty()) {
                val mensagem = Mensagem(
                    dePara = "${auth.currentUser?.uid}_$outroUsuarioId",
                    texto = texto,
                    deUsuarioId = auth.currentUser?.uid ?: "",
                    paraUsuarioId = outroUsuarioId,
                    data = com.google.firebase.Timestamp.now()
                )
                db.collection("mensagens").add(mensagem)
                editTextMensagem.setText("")
            }
        }
    }
}