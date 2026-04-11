<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('contact_messages')) {
            return;
        }
        if (! Schema::hasColumn('contact_messages', 'admin_reply')) {
            Schema::table('contact_messages', function (Blueprint $table) {
                $table->text('admin_reply')->nullable()->after('message');
            });
        }
        if (! Schema::hasColumn('contact_messages', 'replied_at')) {
            Schema::table('contact_messages', function (Blueprint $table) {
                $table->timestamp('replied_at')->nullable()->after('admin_reply');
            });
        }
    }

    public function down(): void
    {
        if (! Schema::hasTable('contact_messages')) {
            return;
        }
        if (Schema::hasColumn('contact_messages', 'replied_at')) {
            Schema::table('contact_messages', function (Blueprint $table) {
                $table->dropColumn('replied_at');
            });
        }
        if (Schema::hasColumn('contact_messages', 'admin_reply')) {
            Schema::table('contact_messages', function (Blueprint $table) {
                $table->dropColumn('admin_reply');
            });
        }
    }
};
