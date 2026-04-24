package com.example.meumarketplace.activities
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_cadastro.*

class CadastroActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth
    private lateinit var db: FirebaseFirestore
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cadastro)
        auth = FirebaseAuth.getInstance()
        db = FirebaseFirestore.getInstance()
        btnCadastrar.setOnClickListener {
            val email = editTextEmail.text.toString()
            val senha = editTextSenha.text.toString()
            val nome = editTextNome.text.toString()
            val tipo = if (radioPrestador.isChecked) "prestador" else "cliente"
            auth.createUserWithEmailAndPassword(email, senha)
                .addOnCompleteListener(this) { task ->
                    if (task.isSuccessful) {
                        val user = hashMapOf(
                            "nome" to nome,
                            "email" to email,
                            "tipo" to tipo
                        )
                        db.collection("usuarios").document(auth.currentUser!!.uid).set(user)
                            .addOnSuccessListener {
                                Toast.makeText(this, "Cadastro realizado!", Toast.LENGTH_SHORT).show()
                                finish()
                            }
                    } else {
                        Toast.makeText(this, "Erro no cadastro", Toast.LENGTH_SHORT).show()
                    }
                }
        }
    }
}