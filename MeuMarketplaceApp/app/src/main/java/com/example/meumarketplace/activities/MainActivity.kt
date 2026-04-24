package com.example.meumarketplace.activities
import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.meumarketplace.adapters.AnuncioAdapter
import com.example.meumarketplace.models.Anuncio
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    private lateinit var anuncioAdapter: AnuncioAdapter
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        anuncioAdapter = AnuncioAdapter(mutableListOf())
        recyclerViewAnuncios.layoutManager = LinearLayoutManager(this)
        recyclerViewAnuncios.adapter = anuncioAdapter
        db.collection("anuncios").get()
            .addOnSuccessListener { result ->
                val anuncios = result.toObjects(Anuncio::class.java)
                anuncioAdapter.updateAnuncios(anuncios)
            }
        btnNovoAnuncio.setOnClickListener {
            startActivity(Intent(this, AnuncioActivity::class.java))
        }
        btnPerfil.setOnClickListener {
            startActivity(Intent(this, PerfilActivity::class.java))
        }
        btnChat.setOnClickListener {
            val intent = Intent(this, ChatActivity::class.java)
            intent.putExtra("outroUsuarioId", "ID_DO_USUARIO_AQUI")
            startActivity(intent)
        }
    }
}