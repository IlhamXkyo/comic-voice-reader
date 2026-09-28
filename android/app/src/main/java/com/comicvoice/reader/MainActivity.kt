package com.comicvoice.reader

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.media.projection.MediaProjectionManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.TextView
import android.widget.Toast

class MainActivity : Activity() {

    private val REQUEST_OVERLAY_PERMISSION = 1001
    private val REQUEST_MEDIA_PROJECTION = 1002

    private lateinit var mediaProjectionManager: MediaProjectionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        mediaProjectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager

        // Layout sederhana untuk meminta izin awal
        val layout = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            setPadding(40, 60, 40, 40)
            setBackgroundColor(0xFFFFFFFF.toInt())
        }

        val title = TextView(this).apply {
            text = "COMICVOICE READER (ANDROID)"
            textSize = 20f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            setTextColor(0xFF18181B.toInt())
        }
        layout.addView(title)

        val desc = TextView(this).apply {
            text = "\nAplikasi ini membaca layar komik webtoon secara otomatis saat gulir berhenti.\n\nLangkah pertama: Aktifkan izin jendela mengambang agar balon suara muncul di atas komik."
            textSize = 14f
            setTextColor(0xFF27272A.toInt())
        }
        layout.addView(desc)

        val btnStart = Button(this).apply {
            text = "AKTIFKAN LAYANAN BACA KOMIK"
            setBackgroundColor(0xFFFFE135.toInt())
            setTextColor(0xFF18181B.toInt())
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            setOnClickListener {
                checkAndRequestPermissions()
            }
        }
        layout.addView(btnStart)

        setContentView(layout)
    }

    private fun checkAndRequestPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
            val intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:$packageName")
            )
            startActivityForResult(intent, REQUEST_OVERLAY_PERMISSION)
        } else {
            requestScreenCapture()
        }
    }

    private fun requestScreenCapture() {
        startActivityForResult(
            mediaProjectionManager.createScreenCaptureIntent(),
            REQUEST_MEDIA_PROJECTION
        )
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == REQUEST_OVERLAY_PERMISSION) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
                requestScreenCapture()
            } else {
                Toast.makeText(this, "Izin jendela mengambang dibutuhkan!", Toast.LENGTH_SHORT).show()
            }
        } else if (requestCode == REQUEST_MEDIA_PROJECTION) {
            if (resultCode == RESULT_OK && data != null) {
                // Mulai Floating Bubble Service
                val serviceIntent = Intent(this, FloatingBubbleService::class.java).apply {
                    putExtra("RESULT_CODE", resultCode)
                    putExtra("DATA_INTENT", data)
                }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    startForegroundService(serviceIntent)
                } else {
                    startService(serviceIntent)
                }
                finish() // Tutup activity utama agar pengguna langsung ke layar komik
            } else {
                Toast.makeText(this, "Izin rekam layar dibutuhkan untuk membaca dialog komik.", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
