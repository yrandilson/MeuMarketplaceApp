package com.example.meumarketplace.activities
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_perfil.*

class PerfilActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_perfil)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        val usuarioId = auth.currentUser?.uid ?: return
        db.collection("usuarios").document(usuarioId).get()
            .addOnSuccessListener { document ->
                val usuario = document.toObject(com.example.meumarketplace.models.Usuario::class.java)
                textNome.text = usuario?.nome
                textEmail.text = usuario?.email
                textTipo.text = if (usuario?.tipo == "prestador") "Prestador de Serviço" else "Cliente"
            }
    }
}