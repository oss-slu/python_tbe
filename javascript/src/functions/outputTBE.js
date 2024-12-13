"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var promises_1 = require("fs/promises");
var path = require("path");
/**
 * Outputs the TBE format for the given tables and writes it to a specified directory.
 *
 * @param directory - The directory where the output file will be written.
 * @param tables - An object containing table data, attributes, and comments.
 * @returns A promise that resolves when the file has been written.
 */
var outputTBE = function (directory, tables) { return __awaiter(void 0, void 0, void 0, function () {
    var dataToWrite, dir, err_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                dataToWrite = '';
                dir = path.dirname(directory);
                return [4 /*yield*/, (0, promises_1.mkdir)(dir, { recursive: true })];
            case 1:
                _a.sent();
                _a.label = 2;
            case 2:
                _a.trys.push([2, 4, , 5]);
                Object.keys(tables).forEach(function (table) {
                    var _a;
                    var headers = Object.keys(tables[table].data[0]).join(',');
                    var allRows = tables[table].data.map(function (row) { return Object.values(row); });
                    var lastRow = (_a = allRows.pop()) === null || _a === void 0 ? void 0 : _a.join(',');
                    var rowData = allRows.map(function (row) { return ',' + row.join(','); }).join('\n');
                    var attData = Object.entries(tables[table].att)
                        .map(function (_a) {
                        var key = _a[0], values = _a[1];
                        return "".concat(key, ",").concat(values.join(','));
                    });
                    var cmtData = Object.entries(tables[table].cmt)
                        .map(function (_a) {
                        var key = _a[0], values = _a[1];
                        return "".concat(key, ",").concat(values.join(','));
                    });
                    dataToWrite += "TBL ".concat(table, ",").concat(headers, "\nBGN").concat(rowData, "\nEOT ").concat(table, ",").concat(lastRow, "\n");
                    if (attData.length > 0) {
                        dataToWrite += "ATT ".concat(attData, "\n");
                    }
                    if (cmtData.length > 0) {
                        dataToWrite += "CMT ".concat(cmtData, "\n");
                    }
                    dataToWrite += ',,,\n';
                });
                return [4 /*yield*/, (0, promises_1.writeFile)(directory, dataToWrite)];
            case 3:
                _a.sent();
                return [3 /*break*/, 5];
            case 4:
                err_1 = _a.sent();
                throw err_1;
            case 5: return [2 /*return*/];
        }
    });
}); };
// example usage
var testDirectory = process.argv[2] || './output.csv';
// const exampleTables = {
//     "Users": {
//         "data": [
//             { "Name": "Alice", "Age": "25", "Country": "USA" },
//             { "Name": "Bob", "Age": "30", "Country": "Canada" },
//             { "Name": "Charlie", "Age": "22", "Country": "UK" }
//         ],
//         "att": { "Info": ["Active", "Verified"] },
//         "cmt": { "Notes": ["Test User", "New"] }
//     }
// }
// outputTBE(testDirectory, exampleTables)
// example using real sample_data from '/sample_data'
// sampleData is the stringified object returned by parseTBE()
var main = function () { return __awaiter(void 0, void 0, void 0, function () {
    var sampleData, sampleDataJSON;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, (0, promises_1.readFile)('./src/functions/sampleDataJSON.txt', 'utf-8')];
            case 1:
                sampleData = _a.sent();
                sampleDataJSON = JSON.parse(sampleData);
                outputTBE(testDirectory, sampleDataJSON);
                return [2 /*return*/];
        }
    });
}); };
main();
exports.default = outputTBE;
