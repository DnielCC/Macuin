<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class AddCartLineRequest extends FormRequest
{
    public function authorize(): bool
    {
        return auth()->check();
    }

    public function rules(): array
    {
        return [
            'autoparte_id' => ['required', 'integer', 'min:1'],
            'cantidad' => ['required', 'integer', 'min:1', 'max:999'],
        ];
    }

    public function messages(): array
    {
        return [
            'autoparte_id.required' => 'Producto no válido.',
            'cantidad.max' => 'La cantidad máxima por línea es 999.',
        ];
    }
}
