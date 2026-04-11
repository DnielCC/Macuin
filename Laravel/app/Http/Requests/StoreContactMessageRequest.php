<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreContactMessageRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'min:3', 'max:200'],
            'email' => ['required', 'email', 'max:255'],
            'phone' => ['nullable', 'string', 'max:40', 'regex:/^$|^[\d\s+\-().]{10,40}$/'],
            'subject' => ['required', 'string', 'min:3', 'max:200'],
            'message' => ['required', 'string', 'min:10', 'max:5000'],
        ];
    }

    public function messages(): array
    {
        return [
            'name.required' => 'Indica tu nombre.',
            'email.required' => 'Indica un correo de contacto.',
            'email.email' => 'El correo no tiene un formato válido.',
            'subject.required' => 'Escribe un asunto breve.',
            'message.required' => 'Escribe tu mensaje.',
            'message.min' => 'El mensaje debe tener al menos 10 caracteres.',
            'phone.regex' => 'Si indicas teléfono, usa entre 10 y 40 caracteres (dígitos y + - ( ) .).',
        ];
    }
}
